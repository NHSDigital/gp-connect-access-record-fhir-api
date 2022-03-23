using System.Net.Http;
using System.Net.Http.Headers;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authorization;
using Microsoft.Extensions.Configuration;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;
using System;
using System.Linq;
using System.Collections.Generic;
using Newtonsoft.Json.Linq;
using oauth_nhsd_api.Helpers;

namespace oauth_nhsd_api.Pages
{
    [Authorize]
    public class AllergiesModel : PageModel
    {
        public JToken EntriesAsJson { get; set; }
        public string ResResponse { get; set; }

        public DateTime SessionExpires { get; set; }
        public List<DateNameJsonBundle> OrderedActiveList { get; set; } = new List<DateNameJsonBundle>();

        private readonly IConfiguration _configuration;

        public AllergiesModel(IConfiguration configuration)
        {
            _configuration = configuration;
        }
        public async Task OnGet()
        {

            var tokenAccess = await HttpContext.GetTokenAsync("access_token");
            var tokenRefresh = await HttpContext.GetTokenAsync("refresh_token");
            var tokenExpiresAt = await HttpContext.GetTokenAsync("expires_at");

            HttpRequestMessage req = new HttpRequestMessage(System.Net.Http.HttpMethod.Get,
                _configuration["NHSD:APIEndpoint"] + _configuration["NHSD:NhsNumber"]);

            // make the user restricted request.
            req.Headers.Authorization = new AuthenticationHeaderValue("Bearer", tokenAccess);

            HttpResponseMessage NHSAPIresponse = await new HttpClient().SendAsync(req);

            var ResContent = await NHSAPIresponse.Content.ReadAsStringAsync();

            // Parsing of API response into JSON object
            JObject initialAPIParse = JObject.Parse(ResContent);

            var allergyResponseAsString = Convert.ToString(initialAPIParse["response"]);
            var allergyResponseAsJson = JObject.Parse(allergyResponseAsString);

            EntriesAsJson = allergyResponseAsJson.SelectToken("entry");
            var activeList = new List<DateNameJsonBundle>();

            // Looping to create a list of objects to order
            foreach (JToken resource in EntriesAsJson)
            {
                if (resource.SelectToken("resource.resourceType").ToString() == "AllergyIntolerance"
                    && resource.SelectToken("resource.clinicalStatus.coding[0].code").ToString() == "active")
                {
                    var resourceCode = resource.SelectToken("resource.code");

                    var allergyText = Convert.ToString(
                        resourceCode.SelectToken("coding[0].display")
                        ?? resourceCode.SelectToken("text")
                        ?? "Name not Given");

                    activeList.Add(new DateNameJsonBundle
                    {
                        AssertedDate = (DateTime?)resource.SelectToken("resource.recordedDate"),
                        EndDate = null,
                        AssertedTitle = allergyText.ToString(),
                        JtokenBundle = resource.SelectToken("resource")
                    });
                }
                // Orders the list by date, oldest first
                OrderedActiveList = activeList.OrderBy(x => x.AssertedDate).ToList();
            }

            // variables created to disply info to the user.
            ResResponse = string.Format("{0} - {1}", (int)NHSAPIresponse.StatusCode, NHSAPIresponse.StatusCode);
            SessionExpires = Convert.ToDateTime(tokenExpiresAt);

        }
    }
}
