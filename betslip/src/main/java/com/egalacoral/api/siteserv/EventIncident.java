//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, vhudson-jaxb-ri-2.1-558 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.25 at 12:50:43 PM EEST 
//


package com.egalacoral.api.siteserv;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlElements;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlType;
import javax.xml.datatype.XMLGregorianCalendar;


/**
 * <p>Java class for EventIncident complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="EventIncident">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;choice>
 *         &lt;element ref="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}error" minOccurs="0"/>
 *         &lt;sequence>
 *           &lt;choice maxOccurs="unbounded" minOccurs="0">
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}eventIncidentComment"/>
 *             &lt;element ref="{http://schema.openbet.com/SiteServer/2.16/SSResponse.xsd}eventIncidentParticipant"/>
 *           &lt;/choice>
 *         &lt;/sequence>
 *       &lt;/choice>
 *       &lt;attribute name="id" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="eventId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="eventPeriodId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="eventParticipantId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="incidentCode" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="description" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="relativeTime" type="{http://www.w3.org/2001/XMLSchema}integer" />
 *       &lt;attribute name="absoluteTime" type="{http://www.w3.org/2001/XMLSchema}dateTime" />
 *       &lt;attribute name="xPos" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *       &lt;attribute name="yPos" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *       &lt;attribute name="createDate" type="{http://www.w3.org/2001/XMLSchema}dateTime" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "EventIncident", propOrder = {
    "error",
    "list"
})
public class EventIncident {

    protected Error error;
    @XmlElements({
        @XmlElement(name = "eventIncidentParticipant", type = EventIncidentParticipant.class),
        @XmlElement(name = "eventIncidentComment", type = EventIncidentComment.class)
    })
    protected List<Object> list;
    @XmlAttribute
    protected String id;
    @XmlAttribute
    protected String eventId;
    @XmlAttribute
    protected String eventPeriodId;
    @XmlAttribute
    protected String eventParticipantId;
    @XmlAttribute
    protected String incidentCode;
    @XmlAttribute
    protected String description;
    @XmlAttribute
    protected BigInteger relativeTime;
    @XmlAttribute
    @XmlSchemaType(name = "dateTime")
    protected XMLGregorianCalendar absoluteTime;
    @XmlAttribute
    protected BigDecimal xPos;
    @XmlAttribute
    protected BigDecimal yPos;
    @XmlAttribute
    @XmlSchemaType(name = "dateTime")
    protected XMLGregorianCalendar createDate;

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
     * Gets the value of the list property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the list property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getList().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link EventIncidentParticipant }
     * {@link EventIncidentComment }
     * 
     * 
     */
    public List<Object> getList() {
        if (list == null) {
            list = new ArrayList<Object>();
        }
        return this.list;
    }

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
     * Gets the value of the incidentCode property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getIncidentCode() {
        return incidentCode;
    }

    /**
     * Sets the value of the incidentCode property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setIncidentCode(String value) {
        this.incidentCode = value;
    }

    /**
     * Gets the value of the description property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDescription() {
        return description;
    }

    /**
     * Sets the value of the description property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDescription(String value) {
        this.description = value;
    }

    /**
     * Gets the value of the relativeTime property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getRelativeTime() {
        return relativeTime;
    }

    /**
     * Sets the value of the relativeTime property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setRelativeTime(BigInteger value) {
        this.relativeTime = value;
    }

    /**
     * Gets the value of the absoluteTime property.
     * 
     * @return
     *     possible object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public XMLGregorianCalendar getAbsoluteTime() {
        return absoluteTime;
    }

    /**
     * Sets the value of the absoluteTime property.
     * 
     * @param value
     *     allowed object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public void setAbsoluteTime(XMLGregorianCalendar value) {
        this.absoluteTime = value;
    }

    /**
     * Gets the value of the xPos property.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getXPos() {
        return xPos;
    }

    /**
     * Sets the value of the xPos property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setXPos(BigDecimal value) {
        this.xPos = value;
    }

    /**
     * Gets the value of the yPos property.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getYPos() {
        return yPos;
    }

    /**
     * Sets the value of the yPos property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setYPos(BigDecimal value) {
        this.yPos = value;
    }

    /**
     * Gets the value of the createDate property.
     * 
     * @return
     *     possible object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public XMLGregorianCalendar getCreateDate() {
        return createDate;
    }

    /**
     * Sets the value of the createDate property.
     * 
     * @param value
     *     allowed object is
     *     {@link XMLGregorianCalendar }
     *     
     */
    public void setCreateDate(XMLGregorianCalendar value) {
        this.createDate = value;
    }

}
