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

    public string Spotify_Client_ID { get; set; } = string.Empty;
    public string Spotify_Client_Secret { get; set; } = string.Empty;




}
