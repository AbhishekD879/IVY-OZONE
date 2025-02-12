//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.8-b130911.1802 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.21 at 03:30:49 PM CEST 
//


package com.cora.siteserv;

import java.util.ArrayList;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlElements;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for SSResponse complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="SSResponse">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;choice>
 *         &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}error" minOccurs="0"/>
 *         &lt;sequence>
 *           &lt;choice maxOccurs="unbounded" minOccurs="0">
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}category"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}scorecast"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}rule4"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}healthCheck"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}resultedEvent"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}event"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}drilldownTagTarget"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}lottery"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}drilldownTag"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}externalKeys"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}mediaProvider"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}racingFormEvent"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}localisationToken"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}softwareVersion"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}nSetValue"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}drilldownNode"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}class"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}aggregation"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}sport"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}player"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}pool"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}resultedRace"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}coupon"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}property"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}topBet"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}team"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}blurb"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}externalKeyLookup"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}topXBets"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}translation"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}racingFormOutcome"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}checkpoint"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}pastSummary"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}region"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}news"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}idSetToken"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}racingResult"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}dispSort"/>
 *           &lt;/choice>
 *           &lt;element ref="{http://schema.openbet.com/SiteServer/2.15/SSResponse.xsd}responseFooter"/>
 *         &lt;/sequence>
 *       &lt;/choice>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "SSResponse", propOrder = {
    "error",
    "categoryOrScorecastOrRule4",
    "responseFooter"
})
public class SSResponse {

    protected Error error;
    @XmlElements({
        @XmlElement(name = "category", type = Category.class),
        @XmlElement(name = "scorecast", type = Scorecast.class),
        @XmlElement(name = "rule4", type = Rule4 .class),
        @XmlElement(name = "healthCheck", type = HealthCheck.class),
        @XmlElement(name = "resultedEvent", type = ResultedEvent.class),
        @XmlElement(name = "event", type = Event.class),
        @XmlElement(name = "drilldownTagTarget", type = DrilldownTagTarget.class),
        @XmlElement(name = "lottery", type = Lottery.class),
        @XmlElement(name = "drilldownTag", type = DrilldownTag.class),
        @XmlElement(name = "externalKeys", type = ExternalKeys.class),
        @XmlElement(name = "mediaProvider", type = MediaProvider.class),
        @XmlElement(name = "racingFormEvent", type = RacingFormEvent.class),
        @XmlElement(name = "localisationToken", type = LocalisationToken.class),
        @XmlElement(name = "softwareVersion", type = SoftwareVersion.class),
        @XmlElement(name = "nSetValue", type = NSetValue.class),
        @XmlElement(name = "drilldownNode", type = DrilldownNode.class),
        @XmlElement(name = "class", type = Class.class),
        @XmlElement(name = "aggregation", type = Aggregation.class),
        @XmlElement(name = "sport", type = Sport.class),
        @XmlElement(name = "player", type = Player.class),
        @XmlElement(name = "pool", type = Pool.class),
        @XmlElement(name = "resultedRace", type = ResultedRace.class),
        @XmlElement(name = "coupon", type = Coupon.class),
        @XmlElement(name = "property", type = Property.class),
        @XmlElement(name = "topBet", type = TopBet.class),
        @XmlElement(name = "team", type = Team.class),
        @XmlElement(name = "blurb", type = Blurb.class),
        @XmlElement(name = "externalKeyLookup", type = ExternalKeyLookup.class),
        @XmlElement(name = "topXBets", type = TopXBets.class),
        @XmlElement(name = "translation", type = Translation.class),
        @XmlElement(name = "racingFormOutcome", type = RacingFormOutcome.class),
        @XmlElement(name = "checkpoint", type = Checkpoint.class),
        @XmlElement(name = "pastSummary", type = PastSummary.class),
        @XmlElement(name = "region", type = Region.class),
        @XmlElement(name = "news", type = News.class),
        @XmlElement(name = "idSetToken", type = IdSetToken.class),
        @XmlElement(name = "racingResult", type = RacingResult.class),
        @XmlElement(name = "dispSort", type = DispSort.class)
    })
    protected List<Object> categoryOrScorecastOrRule4;
    protected ResponseFooter responseFooter;

    /**
     * Gets the value of the error property.
     * 
     * @return
     *     possible object is
     *     {@link Error }
     *     
     */
    public Error getError() {
        return error;
    }

    /**
     * Sets the value of the error property.
     * 
     * @param value
     *     allowed object is
     *     {@link Error }
     *     
     */
    public void setError(Error value) {
        this.error = value;
    }

    /**
     * Gets the value of the categoryOrScorecastOrRule4 property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the categoryOrScorecastOrRule4 property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getCategoryOrScorecastOrRule4().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link Category }
     * {@link Scorecast }
     * {@link Rule4 }
     * {@link HealthCheck }
     * {@link ResultedEvent }
     * {@link Event }
     * {@link DrilldownTagTarget }
     * {@link Lottery }
     * {@link DrilldownTag }
     * {@link ExternalKeys }
     * {@link MediaProvider }
     * {@link RacingFormEvent }
     * {@link LocalisationToken }
     * {@link SoftwareVersion }
     * {@link NSetValue }
     * {@link DrilldownNode }
     * {@link Class }
     * {@link Aggregation }
     * {@link Sport }
     * {@link Player }
     * {@link Pool }
     * {@link ResultedRace }
     * {@link Coupon }
     * {@link Property }
     * {@link TopBet }
     * {@link Team }
     * {@link Blurb }
     * {@link ExternalKeyLookup }
     * {@link TopXBets }
     * {@link Translation }
     * {@link RacingFormOutcome }
     * {@link Checkpoint }
     * {@link PastSummary }
     * {@link Region }
     * {@link News }
     * {@link IdSetToken }
     * {@link RacingResult }
     * {@link DispSort }
     * 
     * 
     */
    public List<Object> getCategoryOrScorecastOrRule4() {
        if (categoryOrScorecastOrRule4 == null) {
            categoryOrScorecastOrRule4 = new ArrayList<Object>();
        }
        return this.categoryOrScorecastOrRule4;
    }

    /**
     * Gets the value of the responseFooter property.
     * 
     * @return
     *     possible object is
     *     {@link ResponseFooter }
     *     
     */
    public ResponseFooter getResponseFooter() {
        return responseFooter;
    }

    /**
     * Sets the value of the responseFooter property.
     * 
     * @param value
     *     allowed object is
     *     {@link ResponseFooter }
     *     
     */
    public void setResponseFooter(ResponseFooter value) {
        this.responseFooter = value;
    }

}
