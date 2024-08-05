package com.oxygen.publisher.sportsfeatured.model;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import com.oxygen.publisher.sportsfeatured.model.module.EventInputDTO;
import org.junit.Test;

public class EventInputDTOTest {

  @Test
  public void allFieldsValidation() {

    final EventInputDTO eventInputDTO =
        EventInputDTO.builder()
            .withSportId("16")
            .withModuleId("moduleId")
            .withSegmentId("segmentId")
            .build();

    assertEquals("16", eventInputDTO.getSportId());
    assertTrue(eventInputDTO.getModuleId().isPresent());
    assertEquals("moduleId", eventInputDTO.getModuleId().get());
    assertTrue(eventInputDTO.getSegmentId().isPresent());
    assertEquals("segmentId", eventInputDTO.getSegmentId().get());
  }

  @Test
  public void mandatoryFieldValidation() {

    final EventInputDTO eventInputDTO = EventInputDTO.builder().withSportId("16").build();

    assertEquals("16", eventInputDTO.getSportId());
  }
}
