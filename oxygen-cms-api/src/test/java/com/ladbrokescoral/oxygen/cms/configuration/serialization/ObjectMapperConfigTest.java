package com.ladbrokescoral.oxygen.cms.configuration.serialization;

import java.time.Instant;
import java.time.OffsetDateTime;
import lombok.Data;
import org.assertj.core.api.BDDAssertions;
import org.bson.types.ObjectId;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.json.JsonTest;
import org.springframework.boot.test.json.JacksonTester;
import org.springframework.test.context.junit4.SpringRunner;

@JsonTest
@RunWith(SpringRunner.class)
public class ObjectMapperConfigTest extends BDDAssertions {

  @Autowired private JacksonTester<Serialized> jsonSerialized;
  @Autowired private JacksonTester<Deserialized> jsonDeserialized;

  @Data
  private static class Serialized {
    private final String id;
    private final String date;
  }

  @Data
  private static class Deserialized {
    private final ObjectId id;
    private final Instant date;
  }

  @Test
  public void shouldDeserializeOffsetDateTimeToInstant() throws Exception {

    // given
    OffsetDateTime offset = OffsetDateTime.now();
    Serialized serialized = new Serialized(null, offset.toString());

    // when
    Deserialized deserialized =
        jsonDeserialized.parseObject(jsonSerialized.write(serialized).getJson());

    // then
    assertThat(deserialized.getDate()).isEqualTo(offset.toInstant());
  }

  @Test
  public void shouldSerializeObjectIdToString() throws Exception {

    // given
    ObjectId objectId = new ObjectId();
    Deserialized deserialized = new Deserialized(objectId, null);

    // when
    Serialized serialized =
        jsonSerialized.parseObject(jsonDeserialized.write(deserialized).getJson());

    // then
    assertThat(serialized.getId()).isEqualTo(objectId.toString());
  }
}
