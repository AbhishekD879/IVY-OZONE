package com.entain.oxygen.service;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;

import com.entain.oxygen.exceptions.RTMSException;
import com.entain.oxygen.kafka.GlobalKafkaPublisher;
import java.io.IOException;
import java.net.URISyntaxException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Optional;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.assertj.core.api.WithAssertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class RtmsKafkaPublisherServiceTest implements WithAssertions {

  @InjectMocks RtmsKafkaPublisherService service;

  @Mock private GlobalKafkaPublisher rTMSKafkaPublisher;

  @Test
  void processMessage() {
    String filename = "userPreference/dfUpdate/Df_Update.json";
    String updatedmsg = getData(filename);

    ConsumerRecord<String, String> dfUpdate =
        new ConsumerRecord<>("lcg.upms.rtms.destination", 0, 0, "key", updatedmsg);
    service.processMessage(dfUpdate);
    rTMSKafkaPublisher.publishMessage(dfUpdate.key(), dfUpdate.value(), Optional.empty());
    assertNotNull(dfUpdate);
  }

  @Test
  void processMessageWithException() throws RTMSException {
    String filename = "userPreference/dfUpdate/Df_Update_Exception.json";
    String updatedmsg = getDataException(filename);

    ConsumerRecord<String, String> dfUpdate =
        new ConsumerRecord<>("lcg.upms.rtms.destination", 0, 0, "key", updatedmsg);
    RTMSException thrown =
        assertThrows(
            RTMSException.class,
            () -> service.processMessage(dfUpdate),
            "Expected doThing() to throw, but it didn't");
    // service.processMessage(dfUpdate);
    rTMSKafkaPublisher.publishMessage(dfUpdate.key(), dfUpdate.value(), Optional.empty());
    assertNotNull(dfUpdate);
  }

  private String getData(String filename) {
    String updatedmsg = "";
    try (Stream<String> lines =
        Files.lines(Paths.get(ClassLoader.getSystemResource(filename).toURI()))) {
      updatedmsg = lines.collect(Collectors.joining());
    } catch (IOException | URISyntaxException e) {
      throw new RuntimeException(e);
    }
    return updatedmsg;
  }

  private String getDataException(String filename) {
    String updatedmsg = "";
    try (Stream<String> lines =
        Files.lines(Paths.get(ClassLoader.getSystemResource(filename).toURI()))) {
      updatedmsg = lines.collect(Collectors.joining());
    } catch (IOException | URISyntaxException e) {
      throw new RuntimeException(e);
    }
    return updatedmsg;
  }
}
