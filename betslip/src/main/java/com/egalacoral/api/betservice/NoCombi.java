//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, vhudson-jaxb-ri-2.1-558 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.20 at 09:40:42 PM EEST 
//


package com.egalacoral.api.betservice;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for noCombi complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="noCombi">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="legRef" type="{http://schema.openbet.com/core}entityRef" maxOccurs="unbounded"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "noCombi", namespace = "http://schema.products.sportsbook.openbet.com/betcommon", propOrder = {
    "legRef"
})
public class NoCombi
    implements Serializable
{

    private final static long serialVersionUID = 1L;
    @XmlElement(required = true)
    protected List<EntityRef> legRef;

    /**
     * Gets the value of the legRef property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the legRef property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getLegRef().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link EntityRef }
     * 
     * 
     */
    public List<EntityRef> getLegRef() {
        if (legRef == null) {
            legRef = new ArrayList<EntityRef>();
        }
        return this.legRef;
    }

    public boolean isSetLegRef() {
        return ((this.legRef!= null)&&(!this.legRef.isEmpty()));
    }

    public void unsetLegRef() {
        this.legRef = null;
    }

}
