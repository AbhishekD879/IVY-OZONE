package com.ladbrokescoral.oxygen.cms.configuration.changelogs;

import com.github.cloudyrock.mongock.ChangeLog;
import com.github.cloudyrock.mongock.ChangeSet;
import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import org.springframework.context.annotation.Profile;
import org.springframework.core.env.Environment;

@Profile("DEMO")
@ChangeLog(order = "000")
public class DemoChangeLog {

  @ChangeSet(order = "001", id = "createAdmin", author = "vkulikov")
  public void createAdmin(MongockTemplate mongockTemplate, Environment environment) {

    User admin =
        User.builder()
            .admin(true)
            .email(environment.getRequiredProperty("app.demo.admin.email"))
            .password(environment.getRequiredProperty("app.demo.admin.password"))
            .build();

    mongockTemplate.save(admin);
  }

  @ChangeSet(order = "002", id = "createBrands", author = "vkulikov", failFast = false)
  public void createBrands(MongockTemplate mongockTemplate, Environment environment) {

    Brand bma = new Brand();
    bma.setBrandCode(environment.getRequiredProperty("app.demo.brand.coral.brandcode"));
    bma.setTitle((environment.getRequiredProperty("app.demo.brand.coral.title")));
    bma.setSiteServerEndPoint(
        environment.getRequiredProperty("app.demo.brand.coral.siteServerEndPoint"));

    mongockTemplate.save(bma);

    Brand ladbrokes = new Brand();
    ladbrokes.setBrandCode(environment.getRequiredProperty("app.demo.brand.ladbrokes.brandcode"));
    ladbrokes.setTitle((environment.getRequiredProperty("app.demo.brand.ladbrokes.title")));
    ladbrokes.setSiteServerEndPoint(
        environment.getRequiredProperty("app.demo.brand.ladbrokes.siteServerEndPoint"));

    mongockTemplate.save(ladbrokes);
  }
}
