//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.8-b130911.1802 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.21 at 03:30:49 PM CEST 
//


package com.cora.siteserv;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for EventFact complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="EventFact">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;attribute name="id" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="eventId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="eventParticipantId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="eventPeriodId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="fact" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="factCode" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="name" type="{http://www.w3.org/2001/XMLSchema}string" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "EventFact")
public class EventFact {

    @XmlAttribute(name = "id")
    protected String id;
    @XmlAttribute(name = "eventId")
    protected String eventId;
    @XmlAttribute(name = "eventParticipantId")
    protected String eventParticipantId;
    @XmlAttribute(name = "eventPeriodId")
    protected String eventPeriodId;
    @XmlAttribute(name = "fact")
    protected String fact;
    @XmlAttribute(name = "factCode")
    protected String factCode;
    @XmlAttribute(name = "name")
    protected String name;

    /**
     * Gets the value of the id property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getId() {
        return id;
    }

    /**
     * Sets the value of the id property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setId(String value) {
        this.id = value;
    }

    /**
     * Gets the value of the eventId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getEventId() {
        return eventId;
    }

    /**
     * Sets the value of the eventId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setEventId(String value) {
        this.eventId = value;
    }

    /**
     * Gets the value of the eventParticipantId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getEventParticipantId() {
        return eventParticipantId;
    }

    /**
     * Sets the value of the eventParticipantId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setEventParticipantId(String value) {
        this.eventParticipantId = value;
    }

    /**
     * Gets the value of the eventPeriodId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getEventPeriodId() {
        return eventPeriodId;
    }

    /**
     * Sets the value of the eventPeriodId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setEventPeriodId(String value) {
        this.eventPeriodId = value;
    }

    /**
     * Gets the value of the fact property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getFact() {
        return fact;
    }

    /**
     * Sets the value of the fact property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setFact(String value) {
        this.fact = value;
    }

    /**
     * Gets the value of the factCode property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getFactCode() {
        return factCode;
    }

    /**
     * Sets the value of the factCode property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setFactCode(String value) {
        this.factCode = value;
    }

    /**
     * Gets the value of the name property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getName() {
        return name;
    }

    /**
     * Sets the value of the name property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setName(String value) {
        this.name = value;
    }

}
