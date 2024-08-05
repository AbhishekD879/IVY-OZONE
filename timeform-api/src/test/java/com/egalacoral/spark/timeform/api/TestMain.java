package com.egalacoral.spark.timeform.api;

import com.egalacoral.spark.timeform.api.connectivity.RetryReloginFailOverStrategy;
import com.egalacoral.spark.timeform.model.Entry;
import com.egalacoral.spark.timeform.model.Meeting;
import com.egalacoral.spark.timeform.model.Race;
import org.junit.Ignore;
import org.junit.Test;

import java.util.Date;
import java.util.List;

public class TestMain {

  @Ignore
  @Test
  public void test() throws InterruptedException {
    TimeFormAPI api =
        new TimeFormAPIBuilder("https://sso.timeform.com", "https://api.timeform.com/GreyhoundRacingApi/odata") //
            .setFailOverStrategy(new RetryReloginFailOverStrategy(3, 2)) //
            .build();
    final TimeFormService service = api.login("TimeformAlerts@galacoral.com", "spark123");
    service.getMeetingsForDate(new Date(), new DataCallback<List<Meeting>>() {

      @Override
      public void onResponse(List<Meeting> data) {
        System.out.println("Meetings: " + data);
        service.getRacesByMeetingId(data.get(0).getMeetingId(), new DataCallback<List<Race>>() {
          @Override
          public void onResponse(List<Race> data) {
            System.out.println("Races: " + data);
            service.getEntriesByRaceId(data.get(0).getRaceId(), new DataCallback<List<Entry>>() {
              @Override
              public void onResponse(List<Entry> data) {
                System.out.println("Entries: " + data);
              }

              @Override
              public void onError(Throwable throwable) {
                throwable.printStackTrace();
              }
            });
          }
          @Override
          public void onError(Throwable throwable) {
            throwable.printStackTrace();
          }
        });
      }
      @Override
      public void onError(Throwable throwable) {
        throwable.printStackTrace();
      }
    });

    Thread.sleep(100000);
  }

}
