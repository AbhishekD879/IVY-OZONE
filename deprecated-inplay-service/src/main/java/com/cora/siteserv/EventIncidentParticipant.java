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
 * <p>Java class for EventIncidentParticipant complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="EventIncidentParticipant">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;attribute name="id" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="eventIncidentId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="eventParticipantId" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="roleCode" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="role" type="{http://www.w3.org/2001/XMLSchema}string" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "EventIncidentParticipant")
public class EventIncidentParticipant {

    @XmlAttribute(name = "id")
    protected String id;
    @XmlAttribute(name = "eventIncidentId")
    protected String eventIncidentId;
    @XmlAttribute(name = "eventParticipantId")
    protected String eventParticipantId;
    @XmlAttribute(name = "roleCode")
    protected String roleCode;
    @XmlAttribute(name = "role")
    protected String role;

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
     * Gets the value of the eventIncidentId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getEventIncidentId() {
        return eventIncidentId;
    }

    /**
     * Sets the value of the eventIncidentId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setEventIncidentId(String value) {
        this.eventIncidentId = value;
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
     * Gets the value of the roleCode property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getRoleCode() {
        return roleCode;
    }

    /**
     * Sets the value of the roleCode property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setRoleCode(String value) {
        this.roleCode = value;
    }

    /**
     * Gets the value of the role property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getRole() {
        return role;
    }

    /**
     * Sets the value of the role property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setRole(String value) {
        this.role = value;
    }

}
