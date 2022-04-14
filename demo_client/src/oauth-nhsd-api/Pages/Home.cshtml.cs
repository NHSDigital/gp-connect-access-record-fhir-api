using Microsoft.AspNetCore.Authorization;
using Microsoft.Extensions.Configuration;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System;
using Microsoft.AspNetCore.Mvc;

namespace oauth_nhsd_api.Pages
{
    [Authorize]
    public class HomeModel : PageModel
    {
        private readonly IConfiguration _configuration;


        public HomeModel(IConfiguration configuration)
        {
            _configuration = configuration;
        }
        public void OnGet()
        {

        }
    }
}
