package com.gvc.oxygen.betreceipts;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.gvc.oxygen.betreceipts.exceptions.JsonSerializeDeserializeException;
import com.gvc.oxygen.betreceipts.handler.BetReceiptsExceptionHandler;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class BetReceiptsExceptionHandlerTest {
  private BetReceiptsExceptionHandler exceptionHandler;

  @Test
  public void testHandleJsonProcessingException() throws Exception {
    exceptionHandler = new BetReceiptsExceptionHandler();
    Assert.assertNotNull(
        exceptionHandler.handleJsonProcessingException(
            new JsonSerializeDeserializeException(
                "Error in Serialization from nextRace obj",
                new JsonProcessingException("error in processing") {})));
  }
}
