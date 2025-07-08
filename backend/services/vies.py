import zeep
import requests
import logging
from requests import Session
from zeep.transports import Transport
from zeep.exceptions import Error as ZeepError
from datetime import datetime
import re

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Отключаем слишком подробное логгирование от библиотеки Zeep
logging.getLogger('zeep').setLevel(logging.WARNING)

WSDL="https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"

def parse_iso_date(date_str):
    """
    Parse an ISO 8601 date string, handling various formats including problematic timezone formats.
    
    Args:
        date_str: The date string to parse
        
    Returns:
        Parsed datetime or None if parsing failed
    """
    if not date_str:
        return None
        
    try:
        # Try standard parsing first
        return datetime.fromisoformat(date_str)
    except ValueError:
        # If that fails, try to handle the problematic format with regex
        try:
            logger.info(f"Attempting to parse problematic date format: {date_str}")
            # Handle format like "2025-07-08+02:00" by removing the timezone part
            match = re.match(r'(\d{4}-\d{2}-\d{2})([+-]\d{2}:\d{2})', date_str)
            if match:
                date_part = match.group(1)
                return datetime.fromisoformat(date_part)
                
            # If that doesn't work, just parse the date part
            return datetime.fromisoformat(date_str.split('+')[0].split('-')[0])
        except Exception as e:
            logger.error(f"Failed to parse date: {date_str}, error: {str(e)}")
            return None

def check_vat(cc:str, vat:str, requester:dict|None=None)->dict:
    """
    Check VAT number validity using the VIES service.
    
    Args:
        cc: Country code (e.g. 'DE')
        vat: VAT number without country code
        requester: Optional requester information
        
    Returns:
        Dict with validation results
    """
    # Create structured response with default values
    result = {
        "countryCode": cc,
        "vatNumber": vat,
        "valid": False,
        "name": "",
        "address": "",
        "requestDate": datetime.now().isoformat(),
        "requestIdentifier": f"req-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    }
    
    try:
        # Create a session with a timeout
        session = Session()
        session.verify = True
        session.timeout = 30
        
        # Configure client options to ignore strict date parsing
        settings = zeep.Settings(strict=False, xml_huge_tree=True)
        
        # Create a standard transport with custom settings
        transport = Transport(session=session, timeout=30)
        client = zeep.Client(WSDL, transport=transport, settings=settings)
        
        # Check if we have requester information to use the more detailed API
        if requester and requester.get("requester_country_code") and requester.get("requester_vat"):
            try:
                logger.info(f"Attempting detailed VAT check for {cc}{vat}")
                # Use the detailed API with requester information
                res = client.service.checkVatApprox(
                    countryCode=cc,
                    vatNumber=vat,
                    requesterCountryCode=requester.get("requester_country_code"),
                    requesterVatNumber=requester.get("requester_vat")
                )
                logger.info("Detailed VAT check successful")
            except Exception as e:
                logger.warning(f"Detailed VAT check failed: {str(e)}. Falling back to simple check.")
                # Fallback to simple check if the detailed check fails
                try:
                    res = client.service.checkVat(countryCode=cc, vatNumber=vat)
                except Exception as inner_e:
                    logger.error(f"Simple VAT check also failed: {str(inner_e)}")
                    raise
        else:
            # Use the simple API without requester information
            logger.info(f"Attempting simple VAT check for {cc}{vat}")
            try:
                res = client.service.checkVat(countryCode=cc, vatNumber=vat)
                logger.info("Simple VAT check successful")
            except Exception as e:
                logger.error(f"Simple VAT check failed: {str(e)}")
                raise
        
        # Process the response from VIES
        try:
            # Manual extraction of response data to avoid date parsing issues
            logger.info("Processing VIES response")
            
            # Access valid property first - this is most important
            if hasattr(res, 'valid'):
                result["valid"] = bool(res.valid)
            else:
                # Some responses might not have the expected structure
                result["valid"] = True  # Assume valid if we got a response without errors
                
            # Try to get other properties if valid
            if result["valid"]:
                # Process name
                if hasattr(res, 'name'):
                    result["name"] = str(res.name) if res.name else ""
                    
                # Process address    
                if hasattr(res, 'address'):
                    result["address"] = str(res.address) if res.address else ""
                    
                # Process requestIdentifier (might not be present)    
                if hasattr(res, 'requestIdentifier'):
                    result["requestIdentifier"] = str(res.requestIdentifier)
                    
                # Process requestDate if available
                if hasattr(res, 'requestDate'):
                    try:
                        date_str = str(res.requestDate)
                        logger.info(f"Original requestDate from VIES: {date_str}")
                        parsed_date = parse_iso_date(date_str)
                        if parsed_date:
                            result["requestDate"] = parsed_date.isoformat()
                    except Exception as date_error:
                        logger.warning(f"Could not process requestDate: {str(date_error)}")
            
            logger.info(f"VAT check result: valid={result['valid']}")
            
        except Exception as e:
            error_msg = f"Error processing VIES response: {str(e)}"
            logger.error(error_msg)
            result["error"] = error_msg
            result["valid"] = False
            
        return result
    except Exception as e:
        # Log and return error information
        error_msg = f"VIES service error: {str(e)}"
        logger.error(error_msg)
        result["valid"] = False
        result["error"] = error_msg
        return result
