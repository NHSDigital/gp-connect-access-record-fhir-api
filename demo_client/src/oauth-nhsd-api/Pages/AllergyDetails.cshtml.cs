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
            ParseResourceToObjectClass parser = new ParseResourceToObjectClass();
            ParsedModel = parser.ParseResourceToObject(passedJsonObject);
            return Page();

        }

    }
}
