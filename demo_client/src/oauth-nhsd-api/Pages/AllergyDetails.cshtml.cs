using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using oauth_nhsd_api.Helpers;

namespace oauth_nhsd_api.Pages
{
    public class AllergyDetailsModel :  PageModel
    {
        public AllergyResource? ParsedModel { get; set; }

        public ActionResult OnGet(string id)
        {
            if (id == null)
            {
                return RedirectToPage("Allergies");
            }
            var sessionData = HttpContext.Session.GetString(id);

            ////Custom datetime layout was needed to parse 
            var dateTimeConverter = new IsoDateTimeConverter { DateTimeFormat = "dd/MM/yyyy HH:mm:ss" };

            var passedJsonObject = JsonConvert.DeserializeObject<DateNameJsonBundle>(sessionData, dateTimeConverter);

            ////Parse the json to a class for use in frontend
            ParseResourceToObjectClass parser = new ParseResourceToObjectClass();
            ParsedModel = parser.ParseResourceToObject(passedJsonObject);

            return Page();
        }

    }
}
