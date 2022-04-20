using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.WebUtilities;
using System.Collections.Generic;
namespace oauth_nhsd_api
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddRazorPages();

            var param = new Dictionary<string, string>() {
                {"response_type", "code"},
                {"client_id", Configuration["ClientId"]},
                {"scope", "nhs-login"},
                {"redirect_uri", Configuration["NHSD:CallbackUrl"]}
            };
            var url = QueryHelpers.AddQueryString("/authorize", param);

            services.AddAuthentication(options =>
                {
                    // Authentication cookie - are you authentciated or not. if not - default challenge scheme defines what should be used to authenticate you
                    // here using custom scheme NHSD
                    options.DefaultAuthenticateScheme = CookieAuthenticationDefaults.AuthenticationScheme;
                    options.DefaultSignInScheme = CookieAuthenticationDefaults.AuthenticationScheme;

                    options.DefaultChallengeScheme = "NHSD";
                })
                .AddCookie(options =>
                {
                    options.Cookie.HttpOnly = true;
                    options.Cookie.SameSite = SameSiteMode.Lax;
                    options.Cookie.SecurePolicy = CookieSecurePolicy.Always;
                    options.ExpireTimeSpan = new System.TimeSpan(0, 10, 0);
                    options.LoginPath = "/Index";
                    options.SlidingExpiration = true;
                })

                
                .AddOAuth("NHSD", options =>
                {
                    // The first oAuth endpoint - where user log in
                    options.AuthorizationEndpoint = Configuration["NHSD:OAuthEndpoint"] + url;

                    // where to send the auth code back to - middleware will create this endpoint
                    options.CallbackPath = new PathString("/callback");

                    // id and secret issued by oAUth provider
                    options.ClientId = Configuration["ClientId"];
                    options.ClientSecret = Configuration["ClientSecret"];

                    // endpoint where we can exchange our auth code for an access token
                    options.TokenEndpoint = Configuration["NHSD:OAuthEndpoint"] + "/token";
                    options.SaveTokens = true;
                });
            services.AddDistributedMemoryCache();

            services.AddSession(options =>
            {
                options.IdleTimeout = System.TimeSpan.FromMinutes(10);
                options.Cookie.HttpOnly = true;
                options.Cookie.IsEssential = true;
                

            });


        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            else
            {
                app.UseExceptionHandler("/Error");
                // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
                app.UseHsts();
            }

            app.UseHttpsRedirection();
            app.UseStaticFiles();

            app.UseCookiePolicy(new CookiePolicyOptions()
            {
                MinimumSameSitePolicy = SameSiteMode.Lax,
                Secure = CookieSecurePolicy.Always
            });

           
            app.UseRouting();

            app.UseAuthentication();
            app.UseAuthorization();
          
            app.UseSession();

            app.UseEndpoints(endpoints =>
            {
                endpoints.MapRazorPages();
            });
        }
    }
}
