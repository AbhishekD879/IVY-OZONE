package middleware.scheduler


import org.springframework.scheduling.TriggerContext
import org.springframework.scheduling.support.CronTrigger
import spock.lang.Specification

class TestConsumeFeaturedDateScheduledSpec extends Specification {
  def "Test scheduler"() {
    CronTrigger trigger =
        new CronTrigger("*/20 * * * * *");
    Date today = Calendar.getInstance().getTime();


    when:
    Date nextExecutionTime = trigger.nextExecutionTime(new TriggerContext() {
          @Override
          Date lastScheduledExecutionTime() {
            return today;
          }

          @Override
          Date lastActualExecutionTime() {
            return today;
          }

          @Override
          Date lastCompletionTime() {
            return today;
          }
        });
    int seconds = nextExecutionTime.getSeconds();

    then: //Assert execution start every 20th second
    seconds * 1 % 20 == 0
  }
}
