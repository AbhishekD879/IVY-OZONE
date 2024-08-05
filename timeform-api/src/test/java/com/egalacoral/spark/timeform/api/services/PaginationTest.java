package com.egalacoral.spark.timeform.api.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

import com.egalacoral.spark.timeform.api.TimeFormException;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.invocation.InvocationOnMock;
import org.mockito.runners.MockitoJUnitRunner;
import org.mockito.stubbing.Answer;

import com.egalacoral.spark.timeform.api.DataCallback;
import com.egalacoral.spark.timeform.api.TimeFormContext;
import com.egalacoral.spark.timeform.api.connectivity.RequestPerformer;
import com.egalacoral.spark.timeform.model.internal.DataResponse;

import retrofit2.Call;

@RunWith(MockitoJUnitRunner.class)
public class PaginationTest {

  private DataService dataService;

  private TimeFormContext context;

  @Mock
  private Function createCallFunction;

  @Mock
  private RequestPerformer requestPerformer;

  @Mock
  private DataCallback dataCallback;

  @Before
  public void setUp() {
    context = new TimeFormContext("http://demo.demo.demo", "http://demo.demo.demo");
    context.setRequestPerformer(requestPerformer);

    dataService = new DataService(context);
  }

  @Test
  public void testPagination() {
    int pageSize = 4;
    int totalCount = 6;
    Call call1 = Mockito.mock(Call.class);
    Call call2 = Mockito.mock(Call.class);
    Call call3 = Mockito.mock(Call.class);

    Mockito.when(createCallFunction.apply(Mockito.any(Map.class))).then(new Answer<Call>() {
      @Override
      public Call answer(InvocationOnMock invocation) throws Throwable {
        Map<String, String> params = (Map) invocation.getArguments()[0];
        String pageSizeParam = params.get("$top");
        String offsetParam = params.get("$skip");
        Assert.assertEquals(String.valueOf(pageSize), pageSizeParam);
        switch (offsetParam) {
          case "0": // 0
            return call1;
          case "1": // 0 + 1
            return call2;
          case "3": // 0 + 1 + 2
            return call3;
          default:
            Assert.fail("Wrong '$skip' parameter requested: " + offsetParam);
        }
        return null;
      }
    });

    DataResponse<Object> response1 = new DataResponse<>();
    DataResponse<Object> response2 = new DataResponse<>();
    DataResponse<Object> response3 = new DataResponse<>();
    response1.setTotalCount(totalCount);
    response2.setTotalCount(totalCount);
    response3.setTotalCount(totalCount);
    response1.setEntities(new ArrayList<Object>() {
      {
        add(new Object());
      }
    });
    response2.setEntities(new ArrayList<Object>() {
      {
        add(new Object());
        add(new Object());
      }
    });
    response3.setEntities(new ArrayList<Object>() {
      {
        add(new Object());
        add(new Object());
        add(new Object());
      }
    });

    // preparation
    // page 1
    Mockito.doAnswer(new Answer() {
      @Override
      public Object answer(InvocationOnMock invocation) throws Throwable {
        ((DataCallback) invocation.getArguments()[1]).onResponse(response1);
        return null;
      }
    }).when(requestPerformer).invokeAsync(Mockito.eq(call1), Mockito.any());
    // page 2
    Mockito.doAnswer(new Answer() {
      @Override
      public Object answer(InvocationOnMock invocation) throws Throwable {
        ((DataCallback) invocation.getArguments()[1]).onResponse(response2);
        return null;
      }
    }).when(requestPerformer).invokeAsync(Mockito.eq(call2), Mockito.any());
    // page 3
    Mockito.doAnswer(new Answer() {
      @Override
      public Object answer(InvocationOnMock invocation) throws Throwable {
        ((DataCallback) invocation.getArguments()[1]).onResponse(response3);
        return null;
      }
    }).when(requestPerformer).invokeAsync(Mockito.eq(call3), Mockito.any());

    // action
    dataService.pagination(createCallFunction, new ArrayList<>(), dataCallback, pageSize);

    // verification
    ArgumentCaptor captor = ArgumentCaptor.forClass(Object.class);
    Mockito.verify(dataCallback).onResponse(captor.capture());
    Object result = captor.getValue();
    Assert.assertTrue(result instanceof List);
    List list = (List) result;
    Assert.assertEquals(totalCount, list.size());
  }

  @Test
  public void testPaginationError() {
    int pageSize = 4;
    int totalCount = 6;
    Call call1 = Mockito.mock(Call.class);
    Call call2 = Mockito.mock(Call.class);

    Mockito.when(createCallFunction.apply(Mockito.any(Map.class))).then(new Answer<Call>() {
      @Override
      public Call answer(InvocationOnMock invocation) throws Throwable {
        Map<String, String> params = (Map) invocation.getArguments()[0];
        String pageSizeParam = params.get("$top");
        String offsetParam = params.get("$skip");
        Assert.assertEquals(String.valueOf(pageSize), pageSizeParam);
        switch (offsetParam) {
          case "0": // 0
            return call1;
          case "1": // 0 + 1
            return call2;
          default:
            Assert.fail("Wrong '$skip' parameter requested: " + offsetParam);
        }
        return null;
      }
    });

    DataResponse<Object> response1 = new DataResponse<>();
    response1.setTotalCount(totalCount);
    response1.setEntities(new ArrayList<Object>() {
      {
        add(new Object());
      }
    });
    TimeFormException tfe = new TimeFormException();

    // preparation
    // page 1
    Mockito.doAnswer(new Answer() {
      @Override
      public Object answer(InvocationOnMock invocation) throws Throwable {
        ((DataCallback) invocation.getArguments()[1]).onResponse(response1);
        return null;
      }
    }).when(requestPerformer).invokeAsync(Mockito.eq(call1), Mockito.any());
    // page 2 -> Error
    Mockito.doAnswer(new Answer() {
      @Override
      public Object answer(InvocationOnMock invocation) throws Throwable {
        ((DataCallback) invocation.getArguments()[1]).onError(tfe);
        return null;
      }
    }).when(requestPerformer).invokeAsync(Mockito.eq(call2), Mockito.any());

    // action
    dataService.pagination(createCallFunction, new ArrayList<>(), dataCallback, pageSize);

    // verification
    ArgumentCaptor<Throwable> captor = ArgumentCaptor.forClass(Throwable.class);
    Mockito.verify(dataCallback, Mockito.never()).onResponse(Mockito.any());
    Mockito.verify(dataCallback).onError(captor.capture());
    Assert.assertEquals(tfe, captor.getValue());
  }

}
