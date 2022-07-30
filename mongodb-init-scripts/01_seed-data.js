// Create user
dbAdmin = db.getSiblingDB("admin");
dbAdmin.createUser({
  user: "tgfp",
  pwd: "test_data_pw",
  roles: [{ role: "userAdminAnyDatabase", db: "admin" }],
  mechanisms: ["SCRAM-SHA-1"],
});

// Authenticate user
dbAdmin.auth({
  user: "tgfp",
  pwd: "test_data_pw",
  mechanisms: ["SCRAM-SHA-1"],
  digestPassword: true,
});

// Create DB and collection
db = new Mongo().getDB("tgfp");
db.createCollection("players", { capped: false });