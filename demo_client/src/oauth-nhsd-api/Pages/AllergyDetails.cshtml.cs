using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using oauth_nhsd_api.Helpers;

namespace oauth_nhsd_api.Pages
{
    [Authorize]
    public class AllergyDetailsModel : PageModel
    {
        public AllergyResource? ParsedModel { get; set; }
        private readonly IsoDateTimeConverter _dateTimeConverter = new() { DateTimeFormat = "dd/MM/yyyy HH:mm:ss" };
        private readonly ParseResourceToObjectClass _parser = new();

        public ActionResult OnGet(string id, string allergyType)
        {
            // If URL is manually navigated to
            if (id == null)
            {
                return RedirectToPage("Allergies");
            }

            // If Query string manually added out of range 
            var sessionData = HttpContext.Session.GetString(allergyType + "_" + id);
            if (sessionData == null)
            {
                return RedirectToPage("Allergies");
            }
            // Custom converter (_dateTimeConverter) required to parse date
            var passedJsonObject = JsonConvert.DeserializeObject<DateNameJsonBundle>(sessionData, _dateTimeConverter);

            ParsedModel = _parser.ParseResourceToObject(passedJsonObject);

            return Page();
        }

    }
}
