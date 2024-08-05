package com.egalacoral.spark.timeform.api;

import com.egalacoral.spark.timeform.api.services.endpoints.params.MeetingDateEq;
import org.junit.Test;

import java.util.Date;

public class MeetingDateEqTest {

  @Test
  public void test() {
    MeetingDateEq eq = new MeetingDateEq(new Date());
    System.out.println(eq.build());
  }

}
