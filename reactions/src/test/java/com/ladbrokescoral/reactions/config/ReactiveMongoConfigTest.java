package com.ladbrokescoral.reactions.config;

import com.mongodb.reactivestreams.client.MongoClient;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class ReactiveMongoConfigTest {

  private ReactiveMongoConfig reactiveMongoConfig;
  private MongoProps mongoProps;

  @BeforeEach
  public void init() {
    mongoProps = mongoProps();
    reactiveMongoConfig = new ReactiveMongoConfig("LOCAL", mongoProps);
  }

  @Test
  void testDataBase() {
    String db = reactiveMongoConfig.getDatabaseName();
    Assertions.assertNotNull(db);
    Assertions.assertTrue(db.equalsIgnoreCase("preferences"));
  }

  @Test
  void testMongoClientWithDefaultUri() {
    MongoClient mongoClient = reactiveMongoConfig.reactiveMongoClient();
    Assertions.assertNotNull(mongoClient);
  }

  @Test
  void testMongoClientWithCredentials() {
    reactiveMongoConfig = new ReactiveMongoConfig("TST0", mongoProps);
    MongoClient mongoClient = reactiveMongoConfig.reactiveMongoClient();
    Assertions.assertNotNull(mongoClient);
  }

  @Test
  void testMongoClientWithoutReplicaAndAuthSource() {
    MongoProps mongoProps = mongoProps();
    mongoProps.setReplicaSet("");
    mongoProps.setAuthSource("");
    reactiveMongoConfig = new ReactiveMongoConfig("TST0", mongoProps);
    MongoClient mongoClient = reactiveMongoConfig.reactiveMongoClient();
    Assertions.assertNotNull(mongoClient);
  }

  @Test
  void testMongoIndexCreation() {
    boolean isIndexCreated = this.reactiveMongoConfig.autoIndexCreation();
    Assertions.assertTrue(isIndexCreated);
  }

  private MongoProps mongoProps() {
    MongoProps mongoDbProperties = new MongoProps();
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
