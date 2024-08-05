package com.entain.oxygen.configuration;

import java.util.ArrayList;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.mongodb.core.ReactiveMongoTemplate;
import org.springframework.data.mongodb.core.index.IndexInfo;
import org.springframework.data.mongodb.core.index.ReactiveIndexOperations;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@ExtendWith(MockitoExtension.class)
class IndexManagerTest {

  @Mock private MongoDbProperties mongoDbProperties;

  @Mock private ReactiveMongoTemplate reactiveMongoTemplate;

  private IndexManager indexManager;

  @BeforeEach
  public void init() {
    this.indexManager = new IndexManager(reactiveMongoTemplate, mongoDbProperties);
  }

  @Test
  void testDropIndex() {
    IndexInfo indexInfo = new IndexInfo(new ArrayList<>(), "username", false, false, "");
    ReactiveIndexOperations reactiveIndexOperations = Mockito.mock(ReactiveIndexOperations.class);
    MongoDbProperties.Index index = new MongoDbProperties.Index();
    index.setCollectionNames("userPreference");
    index.setIndexNames("username");
    Mockito.when(mongoDbProperties.getIndex()).thenReturn(index);
    Mockito.when(reactiveMongoTemplate.indexOps(Mockito.anyString()))
        .thenReturn(reactiveIndexOperations);
    Mockito.when(reactiveIndexOperations.getIndexInfo()).thenReturn(Flux.just(indexInfo));
    Mockito.when(reactiveIndexOperations.dropIndex(Mockito.anyString())).thenReturn(Mono.empty());
    this.indexManager.dropIndex();
    Mockito.verify(reactiveIndexOperations, Mockito.atLeast(1)).dropIndex(Mockito.anyString());
  }

  @Test
  void testDropIndexWithEmptyCollection() {
    MongoDbProperties.Index index = new MongoDbProperties.Index();
    index.setIndexNames("username");
    index.setCollectionNames("");
    Mockito.when(mongoDbProperties.getIndex()).thenReturn(index);
    ReactiveIndexOperations reactiveIndexOperations = Mockito.mock(ReactiveIndexOperations.class);

    this.indexManager.dropIndex();

    Mockito.verifyNoInteractions(reactiveIndexOperations);
  }

  @Test
  void testDropIndexWithEmptyIndexName() {
    IndexInfo indexInfo = new IndexInfo(new ArrayList<>(), "username", true, false, "");
    ReactiveIndexOperations reactiveIndexOperations = Mockito.mock(ReactiveIndexOperations.class);
    MongoDbProperties.Index index = new MongoDbProperties.Index();
    index.setIndexNames("");
    index.setCollectionNames("userPreference");
    Mockito.when(mongoDbProperties.getIndex()).thenReturn(index);
    Mockito.when(reactiveMongoTemplate.indexOps(Mockito.anyString()))
        .thenReturn(reactiveIndexOperations);
    Mockito.when(reactiveIndexOperations.getIndexInfo()).thenReturn(Flux.just(indexInfo));

    this.indexManager.dropIndex();

    Mockito.verify(reactiveIndexOperations, Mockito.atLeast(1)).getIndexInfo();
    Mockito.verify(reactiveIndexOperations, Mockito.times(0)).dropIndex(Mockito.anyString());
  }
}
