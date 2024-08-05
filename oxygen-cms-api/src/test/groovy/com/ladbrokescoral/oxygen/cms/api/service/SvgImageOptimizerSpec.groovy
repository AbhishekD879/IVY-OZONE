package com.ladbrokescoral.oxygen.cms.api.service

import spock.lang.Specification

class SvgImageOptimizerSpec extends Specification {

  public static final String image = "<svg height=\"512\" width=\"512\" xmlns=\"http://www.w3.org/2000/svg\"><circle cx=\"256\" cy=\"256\" fill=\"#bcdefa\" r=\"256\"/><path d=\"M295.495 508.972C418.128 489.981 512 383.953 512 256c0-2.09-.025-4.175-.075-6.253l-58.876-58.876-14.939 11.475-85.578-85.578-21.133 67.881L256 109.25 113.915 327.391z\" fill=\"#92cbf7\"/><path d=\"M241.917 382.96c-96.275-50.74-133.188-169.918-82.449-266.192 96.276 50.739 133.189 169.917 82.449 266.192z\" fill=\"#ff468c\"/><path d=\"M270.083 382.96c96.275-50.74 133.188-169.918 82.449-266.192h-.001c-96.275 50.739-133.188 169.918-82.448 266.192z\" fill=\"#be1964\"/><path d=\"M256 387.919c-108.827 0-197.048-88.221-197.048-197.048C167.779 190.87 256 279.092 256 387.919z\" fill=\"#ff5f96\"/><path d=\"M256 387.919c108.827 0 197.048-88.221 197.048-197.048C344.221 190.87 256 279.092 256 387.919z\" fill=\"#d72878\"/><path d=\"M256 387.919c-76.952-76.952-76.952-201.716 0-278.669 76.952 76.952 76.952 201.717 0 278.669z\" fill=\"#ff73a5\"/><g><path d=\"M256 387.919c.005.005-.005-.005 0 0 76.952-76.952 76.952-201.717 0-278.669z\" fill=\"#ff468c\"/></g></svg>"
  private SvgImageOptimizer svgImageOptimizer;

  def "optimize not enabled"() {
    given:
    svgImageOptimizer = new SvgImageOptimizer(false);

    when:
    def result = svgImageOptimizer.optimize(image)

    then:
    result.get() == image
  }
}
