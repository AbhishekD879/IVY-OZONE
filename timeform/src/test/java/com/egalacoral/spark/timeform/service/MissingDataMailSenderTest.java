package com.egalacoral.spark.timeform.service;

import com.egalacoral.spark.siteserver.model.Type;
import com.egalacoral.spark.timeform.model.LostEvent;
import com.egalacoral.spark.timeform.model.LostOutcome;
import com.egalacoral.spark.timeform.model.MissingTimeFormData;
import com.egalacoral.spark.timeform.service.SiteServerDataWrappers.EventForTest;
import com.egalacoral.spark.timeform.service.SiteServerDataWrappers.MarketForTest;
import com.egalacoral.spark.timeform.service.SiteServerDataWrappers.OutcomeForTest;
import com.egalacoral.spark.timeform.service.SiteServerDataWrappers.TypeForTest;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import javax.mail.Message;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;
import org.apache.velocity.app.VelocityEngine;
import org.apache.velocity.runtime.RuntimeConstants;
import org.apache.velocity.runtime.resource.loader.ClasspathResourceLoader;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.runners.MockitoJUnitRunner;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessagePreparator;

@RunWith(MockitoJUnitRunner.class)
public class MissingDataMailSenderTest {

  @Mock JavaMailSender javaMailSender;

  @Mock MimeMessage mimeMessage;

  private MissingDataMailSender mailSender;

  private MissingTimeFormData missingData;

  @Before
  public void setUp() {
    VelocityEngine velocityEngine = new VelocityEngine();
    velocityEngine.setProperty(RuntimeConstants.RESOURCE_LOADER, "classpath");
    velocityEngine.setProperty(
        "classpath.resource.loader.class", ClasspathResourceLoader.class.getName());

    TypeForTest typeA = new TypeForTest(1, "A");
    TypeForTest typeB = new TypeForTest(2, "B");
    EventForTest event1 = new EventForTest("11", "E1", 1);
    EventForTest event2 = new EventForTest("12", "E2", 2);

    mailSender = new MissingDataMailSender(javaMailSender, velocityEngine);
    List<Type> types = new ArrayList<>();
    types.add(typeA);
    types.add(typeB);

    List<LostEvent> events = new ArrayList<>();
    events.add(new LostEvent(typeA, event1));
    events.add(new LostEvent(typeB, event2));

    List<LostOutcome> outcomes = new ArrayList<>();
    outcomes.add(
        new LostOutcome(
            typeA, event1, new MarketForTest("111", "M1"), new OutcomeForTest("1111", "O1")));
    outcomes.add(
        new LostOutcome(
            typeB, event2, new MarketForTest("112", "M2"), new OutcomeForTest("1112", "O2")));

    missingData = new MissingTimeFormData(new Date(0), types, events, outcomes);
  }

  @Test
  public void testMail() throws Exception {
    mailSender.setSubject("TestSubject <Date>");
    mailSender.setRecipients("a@b.c");
    mailSender.setSenderAddress("d@e.f");

    mailSender.accept(missingData);

    ArgumentCaptor<MimeMessagePreparator> captor =
        ArgumentCaptor.forClass(MimeMessagePreparator.class);
    Mockito.verify(javaMailSender).send(captor.capture());

    MimeMessagePreparator preparator = captor.getValue();
    preparator.prepare(mimeMessage);

    Mockito.verify(mimeMessage).setSubject("TestSubject 1970-01-01", "UTF-8");
    Mockito.verify(mimeMessage)
        .setRecipient(Message.RecipientType.TO, InternetAddress.parse("a@b.c")[0]);
    ;
    Mockito.verify(mimeMessage).setFrom(InternetAddress.parse("d@e.f")[0]);
  }

  @Test
  public void testTwoMails() throws Exception {
    mailSender.setSubject("TestSubject <Date>");
    mailSender.setRecipients("a@b.c,a2@b2.c2");
    mailSender.setSenderAddress("d@e.f");

    mailSender.accept(missingData);

    ArgumentCaptor<MimeMessagePreparator> captor =
        ArgumentCaptor.forClass(MimeMessagePreparator.class);
    Mockito.verify(javaMailSender, Mockito.times(2)).send(captor.capture());

    MimeMessagePreparator preparator = captor.getAllValues().get(0);
    preparator.prepare(mimeMessage);

    Mockito.verify(mimeMessage).setSubject("TestSubject 1970-01-01", "UTF-8");
    Mockito.verify(mimeMessage)
        .setRecipient(Message.RecipientType.TO, InternetAddress.parse("a@b.c")[0]);
    ;
    Mockito.verify(mimeMessage).setFrom(InternetAddress.parse("d@e.f")[0]);

    mimeMessage = Mockito.mock(MimeMessage.class);

    preparator = captor.getAllValues().get(1);
    preparator.prepare(mimeMessage);

    Mockito.verify(mimeMessage).setSubject("TestSubject 1970-01-01", "UTF-8");
    Mockito.verify(mimeMessage)
        .setRecipient(Message.RecipientType.TO, InternetAddress.parse("a2@b2.c2")[0]);
    ;
    Mockito.verify(mimeMessage).setFrom(InternetAddress.parse("d@e.f")[0]);
  }

  @Test
  public void testEmptyRecipients() throws Exception {
    mailSender.setSubject("TestSubject <Date>");
    mailSender.setRecipients(null);

    mailSender.accept(missingData);

    Mockito.verify(javaMailSender, Mockito.never()).send(Mockito.any(MimeMessagePreparator.class));
  }
}
