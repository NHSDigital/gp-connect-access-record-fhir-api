using System;
using System.Net;
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
                OrderedActiveList = GetListFromSessionData();
            }
            else
            {
                var ApiResponse = await GetApiResponse();

                if (ApiResponse == "Failed")
                {
                    Response.Redirect("/Index");

                    foreach (var cookie in HttpContext.Request.Cookies)
                    {
                        Response.Cookies.Delete(cookie.Key);
                    }
                }
                else
                {
                    var UnorderedActiveList = CreateListFromJsonResponse(ApiResponse, "active");

                    OrderedActiveList = UnorderedActiveList.OrderByDescending(listItem => listItem.AssertedDate).ToList();
                }
            }

            SetSessionDataFromList(OrderedActiveList);
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

            if (NHSAPIresponse.StatusCode != HttpStatusCode.Unauthorized)

            {
                var ApiResponse = await NHSAPIresponse.Content.ReadAsStringAsync();

                return ApiResponse;
            }
            else
            {
                return "Failed";
            }
        }

        public void SetSessionDataFromList(List<DateNameJsonBundle> dateNameBundleList)
        {
            if (!IsSessionPopulatedByApiResponse())
            {
                foreach (var dateNameJsonBundle in dateNameBundleList.Select((value, index) => new { value, index }))
                {
                    var dateNameJsonBundleAsString = new Dictionary<string, string>()
                {
                    {"AssertedTitle",  dateNameJsonBundle.value.AssertedTitle},
                    {"AssertedDate", Convert.ToString(dateNameJsonBundle.value.AssertedDate)},
                    {"JtokenBundle", dateNameJsonBundle.value.JtokenBundle}
                };

                    HttpContext.Session.SetString(dateNameJsonBundle.index.ToString(), JsonConvert.SerializeObject(dateNameJsonBundleAsString));
                }
            }
        }

        public List<DateNameJsonBundle> GetListFromSessionData()
        {
            var activeList = new List<DateNameJsonBundle>();
            foreach (var sessionKey in HttpContext.Session.Keys)
            {
                var sessionData = HttpContext.Session.GetString(sessionKey);

                // Custom converter (_dateTimeConverter) required to parse date
                var passedJsonObject = JsonConvert.DeserializeObject<DateNameJsonBundle>(sessionData, _dateTimeConverter);
                activeList.Add(passedJsonObject);
            }
            return activeList;
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
            var response = HttpContext.Session.GetString("0");

            // True: When session entry is present, False: Missing session
            return (response != null);
        }
    }
}
