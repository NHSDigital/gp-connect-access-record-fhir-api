using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Newtonsoft.Json;
using System;
using oauth_nhsd_api.Helpers;

namespace oauth_nhsd_api.Pages
{
    public class AllergyDetailsModel :  PageModel
    {
        public DateNameJsonBundle passedJsonObject { get; set; }
        public AllergyResource ParsedModel { get; set; }

        public IActionResult OnGet(string passedObject)
        {
            passedJsonObject = JsonConvert.DeserializeObject<DateNameJsonBundle>(passedObject);

            if (passedJsonObject == null)
            {
                return NotFound();
            }
            //Parse the json to a class for use in frontend
            ParsedModel = ParseResourceToObject(passedJsonObject);
            return Page();

        }

        public AllergyResource ParseResourceToObject(DateNameJsonBundle resourceBundle)
        {
            var resourceJtoken = resourceBundle.JtokenBundle;
            var resource = new AllergyResource()
            {
                AllergyTitle = Convert.ToString(resourceBundle.AssertedTitle),
                OnSetDate = Convert.ToString(resourceJtoken.SelectToken("onsetDateTime")),
                AssertedDate = Convert.ToString(resourceBundle.AssertedDate),
                EndDate =  Convert.ToString(resourceBundle.EndDate), //This will be added to the bundle upon implementation of "inactive" 
                EndReason = "",
                ClinicalStatus = Convert.ToString(resourceJtoken.SelectToken("resource.clinicalStatus.coding[0].code")),
                AssetType = Convert.ToString(resourceJtoken.SelectToken("type")), //Guessed resource path
                Category = Convert.ToString(resourceJtoken.SelectToken("category[0]")), //Guessed resource path
                Cause = Convert.ToString(resourceJtoken.SelectToken("reaction[0].substance")), //Guessed resource path
                Reaction = Convert.ToString(resourceJtoken.SelectToken("reaction[0].manifestation[0]")), //Guessed resource path
                ReactionSeverity = Convert.ToString(
                    resourceJtoken.SelectToken("criticality")
                    ?? resourceJtoken.SelectToken("reaction[0].severity")), //Guessed resource path,
                AdditionalInformation = Convert.ToString(
                    resourceJtoken.SelectToken("note[0].text")
                    ?? resourceJtoken.SelectToken("reaction[0].note[0]")), //Guessed resource path,
                Recorder = Convert.ToString(resourceJtoken.SelectToken("recorder.reference")), //Guessed resource path
                Asserter = Convert.ToString(resourceJtoken.SelectToken("asserter.reference")), //Guessed resource path
                LastOccurrenceDate = Convert.ToString(resourceJtoken.SelectToken("lastOccurance")), //Guessed resource path
            };
            return resource;
        }
    }
}
