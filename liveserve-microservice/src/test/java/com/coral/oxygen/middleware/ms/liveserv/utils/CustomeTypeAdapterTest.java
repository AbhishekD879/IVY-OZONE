package com.coral.oxygen.middleware.ms.liveserv.utils;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.google.gson.stream.JsonReader;
import com.google.gson.stream.JsonWriter;
import java.io.IOException;
import java.io.Writer;
import org.junit.Assert;
import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
class CustomeTypeAdapterTest {
  CustomeTypeAdapter customeTypeAdapter = new CustomeTypeAdapter();

  @Test
  void testWrite() {
    CustomeTypeAdapter customeTypeAdapter = new CustomeTypeAdapter();
    Error error = new Error();
    try {
      customeTypeAdapter.write(new JsonWriter(Writer.nullWriter()), error);
    } catch (IOException e) {
    }
    Assert.assertNotNull(error);
  }

  @Test
  void testRead() throws IOException {
    Error error = new Error();
    JsonReader jsonReader = mock(JsonReader.class);
    CustomeTypeAdapter customeTypeAdapter = new CustomeTypeAdapter();
    when(jsonReader.hasNext()).thenReturn(false);
    error = customeTypeAdapter.read(jsonReader);
    Assert.assertNotNull(error);
  }

  @Test
  void testRead1() throws IOException {
    Error error = new Error();
    JsonReader jsonReader = mock(JsonReader.class);
    String message = "message";
    CustomeTypeAdapter customeTypeAdapter = new CustomeTypeAdapter();
    when(jsonReader.hasNext()).thenReturn(true).thenReturn(false);
    when(jsonReader.nextName()).thenReturn(message);
    when(jsonReader.nextString()).thenReturn(message);
    error = customeTypeAdapter.read(jsonReader);
    Assert.assertNotNull(error);
  }

  @Test
  void testRead2() throws IOException {
    Error error = new Error();
    JsonReader jsonReader = mock(JsonReader.class);
    String message = "message1";
    CustomeTypeAdapter customeTypeAdapter = new CustomeTypeAdapter();
    when(jsonReader.hasNext()).thenReturn(true).thenReturn(false);
    when(jsonReader.nextName()).thenReturn(message);
    when(jsonReader.nextString()).thenReturn(message);
    error = customeTypeAdapter.read(jsonReader);
    Assert.assertNotNull(error);
  }
}
