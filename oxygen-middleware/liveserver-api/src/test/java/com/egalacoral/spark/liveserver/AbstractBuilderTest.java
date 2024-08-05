package com.egalacoral.spark.liveserver;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.net.URISyntaxException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.function.Function;
import org.junit.Assert;

/** Created by Aliaksei Yarotski on 9/21/17. */
public class AbstractBuilderTest {

  protected static ObjectMapper mapper;
  protected TYPE_DEF thisType;
  protected BaseObject compoundBaseObject;

  static {
    mapper = new ObjectMapper();
    mapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
  }

  protected Message createMessage(TYPE_DEF type, Function<BaseObject, String> messageHeader)
      throws Exception {
    thisType = type;
    BaseObject baseObject = AbstractBuilderTest.read(type.getSource(), BaseObject.class);
    String eventBody = AbstractBuilderTest.write(baseObject.getEvent());
    List<Message> messages =
        new ResponseConverter().convert(messageHeader.apply(baseObject) + eventBody);
    compoundBaseObject = baseObject;
    Assert.assertEquals(1, messages.size());
    Message result = messages.get(0);
    result.setPublishedDate(baseObject.getPublishedDate());
    return result;
  }

  protected static String write(Object object) throws JsonProcessingException {
    return AbstractBuilderTest.mapper.writeValueAsString(object);
  }

  protected static <T> T read(String source, Class<T> targetType) throws IOException {
    return AbstractBuilderTest.mapper.readValue(source, targetType);
  }

  enum UNDEFINED_TYPES { // those messages have been deprecated
    sICENT("sICENT.message"),
    sSTATS("sSTATS.message"),
    COMPAR("COMPAR.message"),
    COMCLS("COMCLS.message"),
    COMSUM("COMSUM.message"),
    COMMSG("COMMSG.message");

    private final String source;

    UNDEFINED_TYPES(String fileName) {
      try {
        Path resource = Paths.get(ClassLoader.getSystemResource(fileName).toURI());
        this.source = new String(Files.readAllBytes(resource));
      } catch (IOException | URISyntaxException e) {
        throw new RuntimeException(e);
      }
    }

    public String getSource() {
      return source;
    }
  }

  enum TYPE_DEF {
    CLOCK("CLOCK_TYPE.json"),
    EVENT("EVENT_TYPE.json"),
    EVMKT("EVMKT_TYPE.json"),
    PRICE("PRICE_TYPE.json"),
    SCBRD("SCBRD_TYPE.json"),
    SELCN("SELCN_TYPE.json");
    private final String source;

    TYPE_DEF(String fileName) {
      try {
        Path resource = Paths.get(ClassLoader.getSystemResource(fileName).toURI());
        this.source = new String(Files.readAllBytes(resource));
      } catch (IOException | URISyntaxException e) {
        throw new RuntimeException(e);
      }
    }

    public String getSource() {
      return source;
    }
  }
}
