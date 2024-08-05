package com.egalacoral.spark.timeform.api;

import com.egalacoral.spark.timeform.api.connectivity.RetryReloginFailOverStrategy;
import com.egalacoral.spark.timeform.api.multiplexer.TimeFormAPIMultiplexer;
import com.egalacoral.spark.timeform.model.greyhound.Entry;
import com.egalacoral.spark.timeform.model.greyhound.Meeting;
import com.egalacoral.spark.timeform.model.greyhound.Performance;
import com.egalacoral.spark.timeform.model.greyhound.Track;
import com.egalacoral.spark.timeform.model.horseracing.HRCourseMap;
import com.egalacoral.spark.timeform.model.horseracing.HRPerformance;
import com.egalacoral.spark.timeform.model.horseracing.HRRace;
import java.io.*;
import java.util.Date;
import java.util.List;
import org.junit.Ignore;
import org.junit.Test;

public class TestMain {

  private TimeFormAPI api =
      new TimeFormAPIBuilder(
              "https://sso.timeform.com",
              "https://" + "api.timeform.com",
              "GreyhoundRacingApi/odata",
              "HorseRacingApi/odata",
              "") //
          .setFailOverStrategy(new RetryReloginFailOverStrategy(3, 2)) //
          .build();

  @Ignore
  @Test
  public void test() throws InterruptedException {
    final TimeFormService service = api.login("TimeformAlerts@galacoral.com", "spark123");
    service.getMeetingsForDate(
        new Date(),
        new DataCallback<List<Meeting>>() {

          @Override
          public void onResponse(List<Meeting> data) {
            System.out.println("Meetings: " + data);
          }

          @Override
          public void onError(Exception e) {
            e.printStackTrace();
          }
        });

    Thread.sleep(100000);
  }

  @Ignore
  @Test
  public void testGetGreyhound() throws Exception {
    final TimeFormService service = api.login("TimeformAlerts@galacoral.com", "spark123");

    service.getEntriesGreyhoundByMeetingDate(
        new Date(),
        new DataCallback<List<Entry>>() {
          @Override
          public void onResponse(List<Entry> data) {
            data.forEach(item -> System.out.println(item.getGreyhound()));
          }

          @Override
          public void onError(Exception e) {
            e.printStackTrace();
          }
        });
    Thread.sleep(100000);
  }

  @Ignore
  @Test
  public void testGetTracks() throws Exception {
    final TimeFormService service = api.login("TimeformAlerts@galacoral.com", "spark123");

    service.getTracks(
        new DataCallback<List<Track>>() {
          @Override
          public void onResponse(List<Track> data) {
            System.out.println(data);
          }

          @Override
          public void onError(Exception e) {
            e.printStackTrace();
          }
        });
    Thread.sleep(1000);
  }

  @Ignore
  @Test
  public void testGetPerformance() throws Exception {
    final TimeFormService service = api.login("TimeformAlerts@galacoral.com", "spark123");

    service.getPerformancesByMeetingDate(
        new Date(),
        new DataCallback<List<Performance>>() {
          @Override
          public void onResponse(List<Performance> data) {
            System.out.println(data);
          }

          @Override
          public void onError(Exception e) {
            e.printStackTrace();
          }
        });
    Thread.sleep(1000);
  }

  @Ignore
  @Test
  public void testGetHRRaces() throws Exception {
    final TimeFormService service = api.login("TimeformAlerts@galacoral.com", "spark123");

    service.getHRRacesWithRacesByMeetingDate(
        new Date(),
        new DataCallback<List<HRRace>>() {
          @Override
          public void onResponse(List<HRRace> data) {
            System.out.println(data);
          }

          @Override
          public void onError(Exception e) {
            e.printStackTrace();
          }
        });
    Thread.sleep(10000);
  }

  @Ignore
  @Test
  public void testGetPerfomances() throws Exception {
    final TimeFormService service = api.login("TimeformAlerts@galacoral.com", "spark123");

    service.getHRPerformancesByMeetingDate(
        new Date(),
        new DataCallback<List<HRPerformance>>() {
          @Override
          public void onResponse(List<HRPerformance> data) {
            System.out.println(data);
          }

          @Override
          public void onError(Exception e) {
            e.printStackTrace();
          }
        });
    Thread.sleep(10000);
  }

  @Ignore
  @Test
  public void testMultiplexer() throws InterruptedException {
    TimeFormAPI api1 =
        new TimeFormAPIBuilder(
                "https://sso.timeform.com",
                "https://api.timeform.com",
                "GreyhoundRacingApi/odata",
                "HorseRacingApi/odata",
                "") //
            .setFailOverStrategy(new RetryReloginFailOverStrategy(3, 2)) //
            .build();
    TimeFormAPI api2 =
        new TimeFormAPIBuilder(
                "https://sso.timeform.com",
                "https://api.timeform.com",
                "GreyhoundRacingApi/odata",
                "HorseRacingApi/odata",
                "") //
            .setFailOverStrategy(new RetryReloginFailOverStrategy(3, 2)) //
            .build();

    TimeFormAPI api = new TimeFormAPIMultiplexer(api1, api2);
    final TimeFormService service = api.login("TimeformAlerts@galacoral.com", "spark123");
    service.getMeetingsForDate(
        new Date(),
        new DataCallback<List<Meeting>>() {

          @Override
          public void onResponse(List<Meeting> data) {
            System.out.println("Meetings: " + data);
          }

          @Override
          public void onError(Exception e) {
            e.printStackTrace();
          }
        });

    Thread.sleep(100000);
  }

  @Ignore
  @Test
  public void testCourseMaps() throws InterruptedException {
    TimeFormAPI api =
        new TimeFormAPIBuilder(
                "https://sso.timeform.com",
                "https://api.timeform.com",
                "GreyhoundRacingApi/odata",
                "HorseRacingApi/odata",
                "https://www.timeform.com") //
            .setFailOverStrategy(new RetryReloginFailOverStrategy(3, 2)) //
            .build();
    final TimeFormService service = api.login("TimeformAlerts@galacoral.com", "spark123");
    service.getHRRacesWithRacesByMeetingDate(
        new Date(),
        new DataCallback<List<HRRace>>() {
          @Override
          public void onResponse(List<HRRace> data) {
            long sum = 0;
            for (HRRace race : data) {
              StringBuilder sb =
                  new StringBuilder(
                      "https://www.timeform.com/racing/downloads/coursemap?courseAbbrev=");
              sb.append(race.getCourseAbbrev());
              sb.append("&raceTypeChar=");
              sb.append(race.getRaceTypeChar());
              sb.append("&raceSurfaceChar=");
              sb.append(race.getRaceSurfaceChar());

              service.getHRCourseMapByRace(
                  race,
                  new DataCallback<HRCourseMap>() {
                    @Override
                    public void onResponse(HRCourseMap data) {
                      File f = new File("CM" + data.getUUID() + "_.png");
                      try {
                        OutputStream os = new FileOutputStream(f);
                        os.write(data.getBytes());
                        os.close();
                      } catch (FileNotFoundException e) {
                        e.printStackTrace();
                      } catch (IOException e) {
                        e.printStackTrace();
                      }
                    }

                    @Override
                    public void onError(Exception throwable) {
                      throwable.printStackTrace();
                    }
                  });
            }
          }

          @Override
          public void onError(Exception throwable) {}
        });

    Thread.sleep(100000);
  }
}
