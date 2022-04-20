using System;
using System.Linq;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Net.Http;
using System.Net.Http.Headers;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using oauth_nhsd_api.Helpers;
using Newtonsoft.Json.Converters;


namespace oauth_nhsd_api.Pages
{
    [Authorize]
    public class AllergiesModel : PageModel
    {
        public List<DateNameJsonBundle> OrderedActiveList { get; set; }
        public List<DateNameJsonBundle> OrderedResolvedList { get; set; }
        private readonly IsoDateTimeConverter _dateTimeConverter = new() { DateTimeFormat = "dd/MM/yyyy HH:mm:ss" };
        private readonly IConfiguration _configuration;

        public AllergiesModel(IConfiguration configuration)
        {
            _configuration = configuration;
        }
        public async Task OnGet()
        {
            if (IsSessionPopulatedByApiResponse())
            {
                OrderedActiveList = GetListFromSessionData("active");
                OrderedResolvedList = GetListFromSessionData("resolved");
            }
            else
            {
                var ApiResponse = await GetApiResponse();

                var UnorderedActiveList = CreateListFromJsonResponse(ApiResponse, "active");
                var UnorderedResolvedList = CreateListFromJsonResponse(ApiResponse, "resolved");

                OrderedActiveList = UnorderedActiveList.OrderByDescending(listItem => listItem.AssertedDate).ToList();
                OrderedResolvedList = UnorderedResolvedList.OrderByDescending(listItem => listItem.AssertedDate).ToList();
            }
            
            SetSessionDataFromList(OrderedActiveList, "active");
            SetSessionDataFromList(OrderedResolvedList, "resolved");
        }

        public async Task<string> GetApiResponse()
        {
            var tokenAccess = await HttpContext.GetTokenAsync("access_token");
            var tokenRefresh = await HttpContext.GetTokenAsync("refresh_token");
            var tokenExpiresAt = await HttpContext.GetTokenAsync("expires_at");

            HttpRequestMessage req = new HttpRequestMessage(System.Net.Http.HttpMethod.Get,
                _configuration["NHSD:APIEndpoint"] + _configuration["NHSD:NhsNumber"]);

            req.Headers.Authorization = new AuthenticationHeaderValue("Bearer", tokenAccess);

            HttpResponseMessage NHSAPIresponse = await new HttpClient().SendAsync(req);

            var ApiResponse = await NHSAPIresponse.Content.ReadAsStringAsync();

            return ApiResponse;
        }

        public void SetSessionDataFromList(List<DateNameJsonBundle> dateNameBundleList, string allergyType)
        {
            if (!IsSessionPopulatedByApiResponse()) {
                foreach (var dateNameJsonBundle in dateNameBundleList.Select((value, index) => new { value, index }))
                {
                    var dateNameJsonBundleAsString = new Dictionary<string, string>()
                {
                    {"AssertedTitle",  dateNameJsonBundle.value.AssertedTitle},
                    {"AssertedDate", Convert.ToString(dateNameJsonBundle.value.AssertedDate)},
                    {"JtokenBundle", dateNameJsonBundle.value.JtokenBundle}
                };

                    HttpContext.Session.SetString(allergyType + "_" + dateNameJsonBundle.index.ToString(), JsonConvert.SerializeObject(dateNameJsonBundleAsString));
                }
            }
        }

        public List<DateNameJsonBundle> GetListFromSessionData(string allergyType)
        {
            var allergyList = new List<DateNameJsonBundle>();
            foreach (var sessionKey in HttpContext.Session.Keys)
            {
                if (sessionKey.Split("_")[0] == allergyType)
                {
                    var sessionData = HttpContext.Session.GetString(sessionKey);

                    // Custom converter (_dateTimeConverter) required to parse date
                    var passedJsonObject = JsonConvert.DeserializeObject<DateNameJsonBundle>(sessionData, _dateTimeConverter);
                    allergyList.Add(passedJsonObject);
                }

                
            }
            return allergyList;
        }

        public List<DateNameJsonBundle> CreateListFromJsonResponse(string apiResponse, string activeStatus)
        {
            JObject initialAPIParse = JObject.Parse(apiResponse);

            var allergyResponseAsString = Convert.ToString(initialAPIParse["response"]);
            var allergyResponseAsJson = JObject.Parse(allergyResponseAsString);

            var EntriesAsJson = allergyResponseAsJson.SelectToken("entry");
            var activeList = new List<DateNameJsonBundle>();


            foreach (JToken resource in EntriesAsJson)
            {
                if (resource.SelectToken("resource.resourceType").ToString() == "AllergyIntolerance"
                    && resource.SelectToken("resource.clinicalStatus.coding[0].code").ToString() == activeStatus)
                {
                    var resourceCode = resource.SelectToken("resource.code");

                    var allergyText = Convert.ToString(
                        resourceCode.SelectToken("coding[0].display")
                        ?? resourceCode.SelectToken("text"));

                    activeList.Add(new DateNameJsonBundle
                    {
                        AssertedDate = (DateTime?)resource.SelectToken("resource.recordedDate"),
                        EndDate = null,
                        AssertedTitle = allergyText.ToString(),
                        JtokenBundle = JsonConvert.SerializeObject(resource.SelectToken("resource"))
                    });
                }
            }

            return activeList;
        }

        public Boolean IsSessionPopulatedByApiResponse()
        {
            var isActiveSessionAvailable = HttpContext.Session.GetString("active_0") != null;
            var isResolvedSessionAvailable = HttpContext.Session.GetString("resolved_0") != null ;

            // True: When session entry is present, False: Missing session
            return isActiveSessionAvailable | isResolvedSessionAvailable;
        }
    }
   
}
