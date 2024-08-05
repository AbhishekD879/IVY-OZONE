package com.egalacoral.spark.timeform.service;

import com.egalacoral.spark.timeform.api.tools.Tools;
import com.egalacoral.spark.timeform.model.MissingTimeFormData;
import java.io.StringWriter;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Collections;
import java.util.Date;
import java.util.List;
import java.util.function.Consumer;
import java.util.stream.Collectors;
import org.apache.velocity.Template;
import org.apache.velocity.VelocityContext;
import org.apache.velocity.app.VelocityEngine;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.mail.javamail.MimeMessagePreparator;
import org.springframework.stereotype.Component;

@Component
public class MissingDataMailSender implements Consumer<MissingTimeFormData> {

  private static final transient Logger LOGGER =
      LoggerFactory.getLogger(MissingDataMailSender.class);

  private final JavaMailSender mailSender;

  private final VelocityEngine velocityEngine;

  private String subject = "Missing Timeform Data - <Date>";

  private String senderAddress = "timeform@galacoral.com";

  private List<String> recipients = Collections.emptyList();

  @Autowired
  public MissingDataMailSender(JavaMailSender mailSender, VelocityEngine velocityEngine) {
    this.mailSender = mailSender;
    this.velocityEngine = velocityEngine;
  }

  @Override
  public void accept(MissingTimeFormData missingTimeFormData) {
    Template template = velocityEngine.getTemplate("templates/missing_data_mail.vm", "UTF-8");
    VelocityContext context = new VelocityContext();
    context.put("data", missingTimeFormData);
    context.put("title", getSportClassName());
    StringWriter writer = new StringWriter();
    template.merge(context, writer);

    String mailBody = writer.toString();

    recipients.forEach(
        recipient -> {
          try {
            MimeMessagePreparator preparator =
                mimeMessage -> {
                  MimeMessageHelper message = new MimeMessageHelper(mimeMessage, "UTF-8");
                  message.setSubject(formatSubject(missingTimeFormData.getDate()));
                  message.setFrom(senderAddress);
                  message.setTo(recipient);
                  message.setText(mailBody, true);
                };
            LOGGER.warn(
                "Sending mail to {} about missing data for {}",
                recipient,
                missingTimeFormData.getDate());
            mailSender.send(preparator);
          } catch (Exception e) {
            LOGGER.error("Mail sending failed", e);
          }
        });
  }

  protected String getSportClassName() {
    return "Greyhounds - Live";
  }

  private String formatSubject(Date date) {
    SimpleDateFormat simpleDateFormat = Tools.simpleDateFormat("yyyy-MM-dd");
    String dateStr = simpleDateFormat.format(date);
    String formatedSubject = subject.replace("<Date>", dateStr);
    return formatedSubject;
  }

  @Value("${missing.data.mail.subject}")
  public void setSubject(String subject) {
    this.subject = subject;
  }

  @Value("${missing.data.mail.sender}")
  public void setSenderAddress(String senderAddress) {
    this.senderAddress = senderAddress;
  }

  @Value("${missing.data.mail.recipients:#{null}}")
  public void setRecipients(String recipientsAddresses) {
    if (recipientsAddresses == null) {
      recipients = Collections.emptyList();
    } else {
      recipients =
          Arrays.stream(recipientsAddresses.split(",")) //
              .map(String::trim) //
              .filter(s -> !s.isEmpty()) //
              .collect(Collectors.toList());
    }
  }
}
