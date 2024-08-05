package com.ladbrokescoral.oxygen.cms.configuration;

import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.JsonSerializer;
import com.fasterxml.jackson.databind.SerializerProvider;
import com.fasterxml.jackson.datatype.jsr310.deser.InstantDeserializer;
import java.io.IOException;
import java.time.Instant;
import java.time.OffsetDateTime;
import org.bson.types.ObjectId;
import org.springframework.boot.jackson.JsonComponent;
import org.springframework.util.StringUtils;

@JsonComponent
public class ObjectMapperConfig {

  public static class ObjectIdSerializer extends JsonSerializer<ObjectId> {

    @Override
    public void serialize(ObjectId value, JsonGenerator gen, SerializerProvider serializers)
        throws IOException {

      serializers.defaultSerializeValue(value.toString(), gen);
    }
  }

  public static class InstantOffsetDeserializer extends JsonDeserializer<Instant> {

    @Override
    public Instant deserialize(JsonParser p, DeserializationContext ctxt) throws IOException {

      OffsetDateTime dateTime = null;

      if (StringUtils.hasText(p.getText())) {
        dateTime = InstantDeserializer.OFFSET_DATE_TIME.deserialize(p, ctxt);
      }

      return dateTime != null ? dateTime.toInstant() : null;
    }
  }
}
