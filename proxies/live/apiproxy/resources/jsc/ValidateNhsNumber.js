valid_nhs_number = false
var id_token_nhs_number = context.getVariable('jwt.DecodeJWT.DecodeIdToken.claim.nhs_number')
var request_pathsuffix = context.getVariable('request.queryparam.patient');

function parse_url(url) {
    var pattern = RegExp("[0-9]{10}");
    var matches =  url.match(pattern);
    return matches
} 

var request_path_nhs_number = parse_url(request_pathsuffix);

if (request_path_nhs_number == id_token_nhs_number){
    valid_nhs_number = true
}

context.setVariable('valid_nhs_number', valid_nhs_number);
