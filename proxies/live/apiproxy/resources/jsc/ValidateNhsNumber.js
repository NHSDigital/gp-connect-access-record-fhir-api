var valid_nhs_number = false
var valid_patient_query_parameter = true
var client_nhs_number = context.getVariable('jwt.DecodeJWT.DecodeIdToken.claim.nhs_number')
var patient_url = context.getVariable('request.queryparam.patient');

function validate_patient_query_parameter(url) {
    /*
      Check the url pased on the patient query parameter follows the spec "https://fhir.nhs.uk/Id/nhs-number"
      url: str
      return: bool
    */
    var pattern = RegExp("^https:\/\/fhir\.nhs\.uk\/Id\/[0-9]{10}$");
    var valid_url =  url.match(pattern);
    return valid_url
}

function extract_nhs_number(url) {
    /*
      Gets a 10 digits number out from a string
      url: str
      return: str
    */
    var pattern = RegExp("[0-9]{10}");
    var matches =  url.match(pattern);
    return matches
} 

if (validate_patient_query_parameter(patient_url)){
    var request_nhs_number = extract_nhs_number(patient_url);
    
    if (request_nhs_number == client_nhs_number){
        valid_nhs_number = true
    }
}else{
    var valid_patient_query_parameter = false
}

print(valid_patient_query_parameter)

context.setVariable('valid_patient_query_parameter', valid_patient_query_parameter);
context.setVariable('valid_nhs_number', valid_nhs_number);
