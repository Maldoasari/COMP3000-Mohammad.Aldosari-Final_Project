using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

public class User
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public ObjectId Id { get; set; }
    public string email_login { get; set; } = string.Empty;
    public string pincode_login { get; set; } = string.Empty;
    public string password_login { get; set; } = string.Empty;

    public string email_service_login_email { get; set; } = string.Empty;
    public string email_service_login_pass { get; set; } = string.Empty;

    public string Netflix_username { get; set; } = string.Empty;
    public string Netflix_pass { get; set; } = string.Empty;

    public string PrimeVideo_username { get; set; } = string.Empty;
    public string PrimeVideo_pass { get; set; } = string.Empty;

    public string Spotify_Client_ID { get; set; } = string.Empty;
    public string Spotify_Client_Secret { get; set; } = string.Empty;




}
