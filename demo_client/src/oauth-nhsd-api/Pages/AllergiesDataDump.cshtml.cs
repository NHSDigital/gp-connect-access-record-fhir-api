using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc.RazorPages;
using oauth_nhsd_api.Helpers;
using System.Collections.Generic;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace oauth_nhsd_api.Pages
{
    public class AllergiesDataDumpModel : PageModel
    {
        public List<AllergyResource> OrderedList { get; set; } = new List<AllergyResource>();
        public AllergyResource Resource { get; set; }
        private ParseResourceToObjectClass _parser = new ParseResourceToObjectClass();
        private IsoDateTimeConverter _dateTimeConverter = new IsoDateTimeConverter { DateTimeFormat = "dd/MM/yyyy HH:mm:ss" };
        public void OnGet()
        {
            foreach (var sessionKey in HttpContext.Session.Keys)
            {
                var SessionJsonAsString = HttpContext.Session.GetString(sessionKey);
                var SessionJsonAsBundle = JsonConvert.DeserializeObject<DateNameJsonBundle>(SessionJsonAsString, _dateTimeConverter);

                OrderedList.Add(_parser.ParseResourceToObject(SessionJsonAsBundle));
            }
        }
    }
}
