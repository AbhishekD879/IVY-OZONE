package com.entain.oxygen.configuration;

import com.mongodb.reactivestreams.client.MongoClient;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class ReactiveMongoConfigTest {

  private ReactiveMongoConfiguration reactiveMongoConfiguration;
  private MongoDbProperties mongoDbProperties;

  @BeforeEach
  public void init() {
    mongoDbProperties = mongoDbProperties();
    reactiveMongoConfiguration =
        new ReactiveMongoConfiguration(
            mongoDbProperties, "default", "mongodb://localhost:27017/preferences");
  }

  @Test
  void testDataBase() {
    String db = reactiveMongoConfiguration.getDatabaseName();
    Assertions.assertNotNull(db);
    Assertions.assertTrue(db.equalsIgnoreCase("preferences"));
  }

  @Test
  void testMongoClientWithDefaultUri() {
    MongoClient mongoClient = reactiveMongoConfiguration.reactiveMongoClient();
    Assertions.assertNotNull(mongoClient);
  }

  @Test
  void testMongoClientWithCredentials() {
    reactiveMongoConfiguration = new ReactiveMongoConfiguration(mongoDbProperties, "high", "");
    MongoClient mongoClient = reactiveMongoConfiguration.reactiveMongoClient();
    Assertions.assertNotNull(mongoClient);
  }

  @Test
  void testMongoClientWithoutReplicaAndAuthSource() {
    MongoDbProperties mongoDbProperties = mongoDbProperties();
    mongoDbProperties.setReplicaSet("");
    mongoDbProperties.setAuthSource("");
    reactiveMongoConfiguration = new ReactiveMongoConfiguration(mongoDbProperties, "high", "");
    MongoClient mongoClient = reactiveMongoConfiguration.reactiveMongoClient();
    Assertions.assertNotNull(mongoClient);
  }

  @Test
  void testMongoIndexCreation() {
    boolean isIndexCreated = this.reactiveMongoConfiguration.autoIndexCreation();
    Assertions.assertTrue(isIndexCreated);
  }

  private MongoDbProperties mongoDbProperties() {
    MongoDbProperties mongoDbProperties = new MongoDbProperties();
    mongoDbProperties.setMongoUser("root");
    mongoDbProperties.setPasswordFile("mongodb/coral/nonprod/preferenceUser.bin");
    mongoDbProperties.setPasswordKeyfile("profilekey.pem");
    mongoDbProperties.setDbHosts("localhost;27017");
    mongoDbProperties.setAlgorithm("DES");
    mongoDbProperties.setAuthSource("admin");
    mongoDbProperties.setReplicaSet("rs0");
    mongoDbProperties.setDbName("preferences");
    return mongoDbProperties;
  }
}
