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
        public JToken JtokenBundle { get; set; }
    }

    public class AllergyResource
    {
        [DisplayName("Allergy")]
        public string AllergyTitle { get; set; } //Code.coding[0].display OR Code.text = ####
        [DisplayName("Onset Date")]
        public string OnSetDate { get; set; } //onsetDateTime = ####
        [DisplayName("Asserted Date")]
        public string AssertedDate { get; set; } //recoredDate = ####
        [DisplayName("End Date")]
        public string EndDate { get; set; }
        [DisplayName("End Reason")]
        public string EndReason { get; set; }
        [DisplayName("Clinical Status")]
        public string ClinicalStatus { get; set; } //ClinicalStatus.coding[0].code = active/inactive
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
}
