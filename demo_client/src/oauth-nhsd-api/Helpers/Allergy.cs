using Newtonsoft.Json.Linq;
using System;
using System.ComponentModel;

namespace oauth_nhsd_api.Helpers
{
    // This entire class should likely be split into multiple parts with better names classes.
    public class DateNameJsonBundle
    {
        public DateTime? AssertedDate { get; set; }
        public DateTime? EndDate { get; set; }
        public string AssertedTitle { get; set; }
        public string JtokenBundle { get; set; }
    }

    public class AllergyResource
    {
        [DisplayName("Allergy")]
        public string AllergyTitle { get; set; } //Code.coding[0].display OR Code.text = ####
        [DisplayName("Id")]
        public string Id { get; set; }
        [DisplayName("Profile")]
        public string Profile { get; set; }
        [DisplayName("Onset Date")]
        public string OnSetDate { get; set; } //onsetDateTime = ####
        [DisplayName("Asserted Date")]
        public string AssertedDate { get; set; } //recoredDate = ####

        [DisplayName("End Date")]
        public string EndDate { get; set; }
        [DisplayName("End Reason")]
        public string EndReason { get; set; }
        [DisplayName("Identifier")]
        public string Identifier { get; set; }
        [DisplayName("Clinical Status")]
        public string ClinicalStatus { get; set; } //ClinicalStatus.coding[0].code = active/inactive
        [DisplayName("Verification Status")]
        public string VerificationStatus { get; set; }
        [DisplayName("Type")]
        public string AssetType { get; set; }
        [DisplayName("Category")]
        public string Category { get; set; } //Category[0] = medication/#####
        [DisplayName("Cause")]
        public string Cause { get; set; }
        [DisplayName("Reaction")]
        public string Reaction { get; set; }
        [DisplayName("Reaction Severity")]
        public string ReactionSeverity { get; set; }
        [DisplayName("Additional Info")]
        public string AdditionalInformation { get; set; } //Code.text = ####
        [DisplayName("Recorder")]
        public string Recorder { get; set; }
        [DisplayName("Asserter")]
        public string Asserter { get; set; }
        [DisplayName("Last Occurance Date")]
        public string LastOccurrenceDate { get; set; }
    }
    public class ParseResourceToObjectClass
    {
        public AllergyResource ParseResourceToObject(DateNameJsonBundle resourceBundle)
        {
            var resourceJtoken = JObject.Parse(resourceBundle.JtokenBundle);

            var resource = new AllergyResource()
            {
                AllergyTitle = Convert.ToString(resourceBundle.AssertedTitle),
                Id = Convert.ToString(resourceJtoken.SelectToken("id")),
                Profile = Convert.ToString(resourceJtoken.SelectToken("meta.profile[0]")),
                OnSetDate = Convert.ToString(resourceJtoken.SelectToken("onsetDateTime")),
                AssertedDate = Convert.ToString(resourceBundle.AssertedDate),
                EndDate = Convert.ToString(resourceBundle.EndDate), //This will be added to the bundle upon implementation of "inactive" 
                EndReason = "",
                Identifier = Convert.ToString(resourceJtoken.SelectToken("identifier[0].value")),
                ClinicalStatus = Convert.ToString(resourceJtoken.SelectToken("resource.clinicalStatus.coding[0].code")),
                VerificationStatus = Convert.ToString(resourceJtoken.SelectToken("verificationStatus.coding[0].code")),
                AssetType = Convert.ToString(resourceJtoken.SelectToken("type")),
                Category = Convert.ToString(resourceJtoken.SelectToken("category[0]")),
                Cause = Convert.ToString(resourceBundle.AssertedTitle),
                Reaction = Convert.ToString(resourceJtoken.SelectToken("reaction[0].manifestation[0].text")),
                ReactionSeverity = Convert.ToString(resourceJtoken.SelectToken("reaction[0].severity")),
                AdditionalInformation = Convert.ToString(
                    resourceJtoken.SelectToken("note[0].text")
                    ?? resourceJtoken.SelectToken("reaction[0].note[0]")),
                Recorder = Convert.ToString(resourceJtoken.SelectToken("recorder.reference")),
                Asserter = Convert.ToString(resourceJtoken.SelectToken("asserter.reference")),
                LastOccurrenceDate = Convert.ToString(resourceJtoken.SelectToken("lastOccurance")),

            };
            return resource;
        }

    }
}
