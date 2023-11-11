using Microsoft.AspNetCore.Authentication;
using Microsoft.Extensions.Options;
using System.Net.Http.Headers;
using System.Security.Claims;
using System.Text.Encodings.Web;
using System.Threading.Tasks;
using System.Linq; // Make sure to include this for Linq methods like FirstOrDefault

public class ApiKeyAuthenticationHandler : AuthenticationHandler<AuthenticationSchemeOptions>
{
    private const string ApiKeyHeaderName = "X-Api-Key";
    private const string ApiKey = "..ccvvc0-9ujhvd54324wsdvkyubv543442xcvybunimin"; // In a real app, get this from a secure place

    public ApiKeyAuthenticationHandler(
        IOptionsMonitor<AuthenticationSchemeOptions> options,
        ILoggerFactory logger,
        UrlEncoder encoder,
        ISystemClock clock)
        : base(options, logger, encoder, clock)
    {
    }

    protected override Task<AuthenticateResult> HandleAuthenticateAsync()
    {
        if (!Request.Headers.TryGetValue(ApiKeyHeaderName, out var apiKeyHeaderValues))
        {
            return Task.FromResult(AuthenticateResult.Fail("API Key was not provided"));
        }

        var providedApiKey = apiKeyHeaderValues.FirstOrDefault();
        if (apiKeyHeaderValues.Count == 0 || providedApiKey != ApiKey)
        {
            return Task.FromResult(AuthenticateResult.Fail("Invalid API Key provided."));
        }

        var claims = new[] { new Claim(ClaimTypes.Name, "ApiKeyUser") };
        var identity = new ClaimsIdentity(claims, nameof(ApiKeyAuthenticationHandler));
        var ticket = new AuthenticationTicket(new ClaimsPrincipal(identity), this.Scheme.Name);
        
        return Task.FromResult(AuthenticateResult.Success(ticket));
    }
}
