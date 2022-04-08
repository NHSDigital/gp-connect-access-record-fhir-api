using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Newtonsoft.Json;
using oauth_nhsd_api.Helpers;
using Newtonsoft.Json.Converters;

namespace oauth_nhsd_api.Pages
{
    public class AllergyDetailsModel :  PageModel
    {
        public AllergyResource? ParsedModel { get; set; }

        public void OnGet()
        {
            var passedObject = HttpContext.Session.GetString("SelectedAllergy");

            //Custom datetime layout was needed to parse 
            var dateTimeConverter = new IsoDateTimeConverter { DateTimeFormat = "dd/MM/yyyy HH:mm:ss" };

            var passedJsonObject = JsonConvert.DeserializeObject<DateNameJsonBundle>(passedObject, dateTimeConverter);

            //Parse the json to a class for use in frontend
            ParseResourceToObjectClass parser = new ParseResourceToObjectClass();
            ParsedModel = parser.ParseResourceToObject(passedJsonObject);
        }

    }
}
