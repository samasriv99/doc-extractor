"""Extraction schemas per document type.

Adding a new document type = add an enum value (core.models.DocumentType),
a schema here, and a prompt in prompts/registry.py. Nothing else changes
(Open/Closed Principle).
"""
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from docextract.core.models import DocumentType


class AadhaarFields(BaseModel):
    name: Optional[str] = None
    aadhaar_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    address: Optional[str] = None


class DrivingLicenseFields(BaseModel):
    name: Optional[str] = None
    license_number: Optional[str] = None
    date_of_birth: Optional[str] = None
    date_of_issue: Optional[str] = None
    valid_until: Optional[str] = None
    address: Optional[str] = None
    vehicle_classes: Optional[str] = None


class ResumeFields(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: Optional[str] = None
    total_experience_years: Optional[str] = None
    latest_employer: Optional[str] = None
    education: Optional[str] = None


SCHEMA_REGISTRY: dict[DocumentType, type[BaseModel]] = {
    DocumentType.AADHAAR: AadhaarFields,
    DocumentType.DRIVING_LICENSE: DrivingLicenseFields,
    DocumentType.RESUME: ResumeFields,
}
