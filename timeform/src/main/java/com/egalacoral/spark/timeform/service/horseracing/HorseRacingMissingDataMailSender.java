package com.egalacoral.spark.timeform.service.horseracing;

import com.egalacoral.spark.timeform.service.MissingDataMailSender;
import org.apache.velocity.app.VelocityEngine;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Component;

@Component
public class HorseRacingMissingDataMailSender extends MissingDataMailSender {

  @Autowired
  public HorseRacingMissingDataMailSender(
      JavaMailSender mailSender, VelocityEngine velocityEngine) {
    super(mailSender, velocityEngine);
  }

  @Value("${horseracing.missing.data.mail.subject}")
  public void setSubject(String subject) {
    super.setSubject(subject);
  }

  @Override
  protected String getSportClassName() {
    return "Horse Racing - Live";
  }
}
