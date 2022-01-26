var valid_nhs_number = false
var client_nhs_number = context.getVariable('jwt.DecodeJWT.DecodeIdToken.claim.nhs_number')
var patient_url = context.getVariable('request.queryparam.patient');

function extract_nhs_number(url) {
    /*
      Gets the nhs number out from a string
      url: str
      return: str
    */
    var pattern = RegExp("[0-9]{10}");
    var matches =  url.match(pattern);
    return matches
} 

var request_nhs_number = extract_nhs_number(patient_url);

if (request_nhs_number == client_nhs_number){
    valid_nhs_number = true
}

context.setVariable('valid_nhs_number', valid_nhs_number);
