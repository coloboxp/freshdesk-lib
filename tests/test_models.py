import pytest

from freshdesk.models.base import FreshdeskModel, PaginatedList
from freshdesk.models.tickets import Ticket
from freshdesk.models.contacts import Contact
from freshdesk.models.companies import Company
from freshdesk.models.agents import Agent
from freshdesk.models.groups import Group
from freshdesk.models.conversations import Conversation
from freshdesk.models.roles import Role
from freshdesk.models.skills import Skill
from freshdesk.models.time_entries import TimeEntry
from freshdesk.models.custom_objects import CustomObjectRecord, CustomObjectSchema
from freshdesk.models.canned_responses import CannedResponse, CannedResponseFolder
from freshdesk.models.discussions import Category, Forum, Topic, Comment
from freshdesk.models.solutions import SolutionCategory, SolutionFolder, SolutionArticle
from freshdesk.models.surveys import Survey, SatisfactionRating
from freshdesk.models.minor_resources import Job, Setting, Thread, ThreadMessage
from freshdesk.models.automations import ScenarioAutomation, SLAPolicy, AutomationRule
from freshdesk.models.fields import Field, TicketField, ContactField, CompanyField
from freshdesk.models.forms_messages import TicketForm, OutboundMessage
from freshdesk.models.admin_resources import (
    Account, BusinessHour, EmailConfig, EmailMailbox, Product,
)
from freshdesk.models.missing_resources import (
    ChannelAvailability, AgentAvailability, AdminGroup,
    OmnichannelActivity, ServiceTask, ServiceGroup, FieldTechnician,
)

TS = "2024-06-15T12:00:00Z"


# ---------------------------------------------------------------------------
# Base models
# ---------------------------------------------------------------------------

class TestBaseModels:
    def test_freshdesk_model_allows_extra(self):
        class Dummy(FreshdeskModel):
            name: str

        m = Dummy(name="x", unexpected=99)
        assert m.name == "x"

    def test_paginated_list(self):
        pl = PaginatedList[int](items=[1, 2], total=5, next_page="http://p2")
        assert pl.items == [1, 2]
        assert pl.total == 5
        assert pl.next_page == "http://p2"

    def test_paginated_list_defaults(self):
        pl = PaginatedList[str](items=[])
        assert pl.total is None
        assert pl.next_page is None


# ---------------------------------------------------------------------------
# Ticket
# ---------------------------------------------------------------------------

class TestTicketModel:
    def test_required_fields(self):
        t = Ticket.model_validate({
            "id": 10, "subject": "Crash", "priority": 4, "status": 2,
            "source": 1, "requester_id": 55,
            "created_at": TS, "updated_at": TS,
        })
        assert t.id == 10
        assert t.subject == "Crash"
        assert t.priority == 4
        assert t.requester_id == 55

    def test_defaults(self):
        t = Ticket.model_validate({
            "id": 1, "subject": "X", "priority": 1, "status": 2,
            "source": 1, "requester_id": 1,
            "created_at": TS, "updated_at": TS,
        })
        assert t.attachments == []
        assert t.cc_emails == []
        assert t.custom_fields == {}
        assert t.deleted is False
        assert t.spam is False
        assert t.fr_escalated is False
        assert t.is_escalated is False
        assert t.fwd_emails == []
        assert t.reply_cc_emails == []
        assert t.tags == []
        assert t.to_emails is None
        assert t.company_id is None
        assert t.description is None
        assert t.email is None
        assert t.group_id is None
        assert t.phone is None
        assert t.type is None


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------

class TestContactModel:
    def test_validate(self):
        c = Contact.model_validate({
            "id": 3, "name": "Jane",
            "created_at": TS, "updated_at": TS,
        })
        assert c.id == 3
        assert c.name == "Jane"
        assert c.active is False
        assert c.deleted is False
        assert c.email is None
        assert c.tags == []
        assert c.other_emails == []
        assert c.other_companies == []


# ---------------------------------------------------------------------------
# Company
# ---------------------------------------------------------------------------

class TestCompanyModel:
    def test_validate(self):
        c = Company.model_validate({
            "id": 7, "name": "Acme",
            "created_at": TS, "updated_at": TS,
        })
        assert c.name == "Acme"
        assert c.domains == []
        assert c.custom_fields == {}
        assert c.description is None
        assert c.health_score is None


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

class TestAgentModel:
    def test_validate(self):
        a = Agent.model_validate({
            "id": 5, "ticket_scope": 1,
            "created_at": TS, "updated_at": TS,
        })
        assert a.id == 5
        assert a.available is False
        assert a.occasional is False
        assert a.group_ids == []
        assert a.role_ids == []
        assert a.name is None


# ---------------------------------------------------------------------------
# Group
# ---------------------------------------------------------------------------

class TestGroupModel:
    def test_validate(self):
        g = Group.model_validate({
            "id": 2, "name": "Support",
            "created_at": TS, "updated_at": TS,
        })
        assert g.name == "Support"
        assert g.description is None
        assert g.escalate_to is None


# ---------------------------------------------------------------------------
# Conversation
# ---------------------------------------------------------------------------

class TestConversationModel:
    def test_validate(self):
        c = Conversation.model_validate({
            "id": 99, "source": 0, "ticket_id": 10, "user_id": 5,
            "created_at": TS, "updated_at": TS,
        })
        assert c.id == 99
        assert c.incoming is False
        assert c.private is False
        assert c.attachments == []
        assert c.to_emails == []
        assert c.cc_emails == []
        assert c.bcc_emails == []
        assert c.body is None


# ---------------------------------------------------------------------------
# Simple named models (id + name + timestamps) – parametrized
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("model_cls,extra", [
    (Role, {"default": False}),
    (Skill, {}),
    (Category, {}),
    (ScenarioAutomation, {}),
    (SLAPolicy, {}),
    (TicketForm, {}),
    (ServiceGroup, {}),
])
def test_simple_named_model(model_cls, extra):
    data = {"id": 1, "name": "Test", "created_at": TS, "updated_at": TS, **extra}
    obj = model_cls.model_validate(data)
    assert obj.id == 1
    assert obj.name == "Test"


# ---------------------------------------------------------------------------
# TimeEntry
# ---------------------------------------------------------------------------

class TestTimeEntryModel:
    def test_validate(self):
        te = TimeEntry.model_validate({
            "id": 1, "ticket_id": 10, "time_spent": "01:30",
            "executed_at": TS, "start_time": TS,
            "created_at": TS, "updated_at": TS,
        })
        assert te.time_spent == "01:30"
        assert te.billable is False
        assert te.timer_running is False
        assert te.custom_fields == {}


# ---------------------------------------------------------------------------
# CustomObject models
# ---------------------------------------------------------------------------

class TestCustomObjectModels:
    def test_record(self):
        r = CustomObjectRecord.model_validate({"id": "rec-1", "data": {"field": "val"}})
        assert r.id == "rec-1"
        assert r.data["field"] == "val"

    def test_schema(self):
        s = CustomObjectSchema.model_validate({
            "id": "sch-1", "name": "Assets", "description": "IT assets",
            "fields": [{"name": "serial", "type": "text"}],
        })
        assert s.name == "Assets"
        assert len(s.fields) == 1


# ---------------------------------------------------------------------------
# CannedResponse models
# ---------------------------------------------------------------------------

class TestCannedResponseModels:
    def test_response(self):
        cr = CannedResponse.model_validate({
            "id": 1, "title": "Greet", "content": "Hi {{name}}",
            "content_html": "<p>Hi {{name}}</p>",
            "created_at": TS, "updated_at": TS,
        })
        assert cr.title == "Greet"
        assert cr.folder_id is None

    def test_folder(self):
        f = CannedResponseFolder.model_validate({
            "id": 1, "name": "General",
        })
        assert f.responses_count == 0
        assert f.created_at is None
        assert f.updated_at is None


# ---------------------------------------------------------------------------
# Discussion models
# ---------------------------------------------------------------------------

class TestDiscussionModels:
    def test_forum(self):
        f = Forum.model_validate({
            "id": 1, "name": "Ideas", "category_id": 2,
            "forum_visibility": 1,
            "created_at": TS, "updated_at": TS,
        })
        assert f.topics_count == 0

    def test_topic(self):
        t = Topic.model_validate({
            "id": 1, "title": "Suggestion", "forum_id": 2,
            "created_at": TS, "updated_at": TS,
        })
        assert t.hits == 0
        assert t.locked is False
        assert t.pinned is False

    def test_comment(self):
        c = Comment.model_validate({
            "id": 1, "body": "Good idea", "topic_id": 3, "user_id": 5,
            "created_at": TS, "updated_at": TS,
        })
        assert c.body_text is None


# ---------------------------------------------------------------------------
# Solution models
# ---------------------------------------------------------------------------

class TestSolutionModels:
    def test_category(self):
        sc = SolutionCategory.model_validate({
            "id": 1, "name": "FAQ",
            "created_at": TS, "updated_at": TS,
        })
        assert sc.visible_in_portals == []

    def test_folder(self):
        sf = SolutionFolder.model_validate({
            "id": 1, "name": "Basics", "category_id": 2, "visibility": 1,
            "created_at": TS, "updated_at": TS,
        })
        assert sf.company_ids == []

    def test_article(self):
        sa = SolutionArticle.model_validate({
            "id": 1, "title": "How to", "description": "Steps",
            "status": 2,
            "created_at": TS, "updated_at": TS,
        })
        assert sa.hits == 0
        assert sa.tags == []
        assert sa.seo_data is None


# ---------------------------------------------------------------------------
# Survey models
# ---------------------------------------------------------------------------

class TestSurveyModels:
    def test_survey(self):
        s = Survey.model_validate({
            "id": 1, "title": "CSAT",
            "created_at": TS, "updated_at": TS,
        })
        assert s.active is False

    def test_satisfaction_rating(self):
        sr = SatisfactionRating.model_validate({
            "id": 1, "agent_id": 2, "user_id": 3,
            "survey_id": 5, "ticket_id": 6,
            "ratings": {"default_question": 103},
            "created_at": TS, "updated_at": TS,
        })
        assert sr.ratings == {"default_question": 103}
        assert sr.feedback is None


# ---------------------------------------------------------------------------
# Minor resource models
# ---------------------------------------------------------------------------

class TestMinorResourceModels:
    def test_job(self):
        j = Job.model_validate({
            "id": "job-1", "status": "completed", "type": "export",
            "created_at": TS, "updated_at": TS,
        })
        assert j.processed_count is None
        assert j.total_count is None

    def test_setting(self):
        s = Setting.model_validate({
            "primary_language": "en",
            "supported_languages": ["ru-RU", "es"],
            "portal_languages": ["ru-RU"],
        })
        assert s.primary_language == "en"
        assert s.supported_languages == ["ru-RU", "es"]
        assert s.helpdesk_url is None
        assert s.name is None

    def test_thread(self):
        t = Thread.model_validate({
            "id": 1, "subject": "Chat", "ticket_id": 10,
            "created_at": TS, "updated_at": TS,
        })
        assert t.participants == []

    def test_thread_message(self):
        tm = ThreadMessage.model_validate({
            "id": 1, "thread_id": 2, "body": "Hello", "user_id": 3,
            "created_at": TS, "updated_at": TS,
        })
        assert tm.body_text is None


# ---------------------------------------------------------------------------
# Automation models
# ---------------------------------------------------------------------------

class TestAutomationModels:
    def test_automation_rule(self):
        ar = AutomationRule.model_validate({
            "id": 1, "name": "Auto-assign", "position": 1, "active": True,
            "created_at": TS, "updated_at": TS,
        })
        assert ar.active is True


# ---------------------------------------------------------------------------
# Field models
# ---------------------------------------------------------------------------

class TestFieldModels:
    def test_field_base(self):
        f = Field.model_validate({
            "id": 1, "name": "status", "label": "Status",
            "position": 1, "type": "default_status",
            "created_at": TS, "updated_at": TS,
        })
        assert f.portal_cc is False
        assert f.portal_cc_to == "requester"
        assert f.choices is None

    def test_ticket_field(self):
        tf = TicketField.model_validate({
            "id": 1, "name": "priority", "label": "Priority",
            "position": 2, "type": "default_priority",
            "created_at": TS, "updated_at": TS,
        })
        assert isinstance(tf, Field)

    def test_contact_field(self):
        cf = ContactField.model_validate({
            "id": 1, "name": "email", "label": "Email",
            "position": 1, "type": "default_email",
            "created_at": TS, "updated_at": TS,
        })
        assert isinstance(cf, Field)

    def test_company_field(self):
        cf = CompanyField.model_validate({
            "id": 1, "name": "name", "label": "Name",
            "position": 1, "type": "default_name",
            "created_at": TS, "updated_at": TS,
        })
        assert isinstance(cf, Field)


# ---------------------------------------------------------------------------
# Forms / Messages models
# ---------------------------------------------------------------------------

class TestFormsMessagesModels:
    def test_outbound_message(self):
        om = OutboundMessage.model_validate({
            "id": 1, "body": "Hey", "channel_id": 2,
            "recipient_id": 3, "user_id": 4,
            "created_at": TS, "updated_at": TS,
        })
        assert om.body == "Hey"


# ---------------------------------------------------------------------------
# Admin resource models
# ---------------------------------------------------------------------------

class TestAdminResourceModels:
    def test_account(self):
        a = Account.model_validate({
            "id": 1, "name": "Acme", "system_name": "acme",
            "helpdesk_url": "https://acme.freshdesk.com",
            "portal_url": "https://acme.freshdesk.com/portal",
            "created_at": TS, "updated_at": TS,
        })
        assert a.primary_contact_id is None

    def test_business_hour(self):
        bh = BusinessHour.model_validate({
            "id": 1, "name": "Default", "time_zone": "UTC",
            "created_at": TS, "updated_at": TS,
        })
        assert bh.business_hours == {}

    def test_email_config(self):
        ec = EmailConfig.model_validate({
            "id": 1, "name": "Support", "reply_email": "s@x.com",
            "created_at": TS, "updated_at": TS,
        })
        assert ec.primary is False

    def test_email_mailbox(self):
        em = EmailMailbox.model_validate({
            "id": 1, "name": "Main", "support_email": "s@x.com",
            "created_at": TS, "updated_at": TS,
        })
        assert em.product_id is None
        assert em.group_id is None

    def test_product(self):
        p = Product.model_validate({
            "id": 1, "name": "Widget",
            "created_at": TS, "updated_at": TS,
        })
        assert p.description is None
        assert p.primary_email is None


# ---------------------------------------------------------------------------
# Missing resource models
# ---------------------------------------------------------------------------

class TestMissingResourceModels:
    def test_channel_availability(self):
        ca = ChannelAvailability.model_validate({
            "category": "chat",
            "availability_status": "online",
            "availability_updated_at": TS,
        })
        assert ca.category == "chat"

    def test_agent_availability(self):
        aa = AgentAvailability.model_validate({
            "agent_id": 1,
            "availability_status": "online",
            "availability_updated_at": TS,
            "availability_control": "manual",
        })
        assert aa.channel_availability == []

    def test_admin_group(self):
        ag = AdminGroup.model_validate({
            "id": 1, "name": "Admins", "type": "support",
            "created_at": TS, "updated_at": TS,
        })
        assert ag.agent_ids == []
        assert ag.allow_agents_to_change_availability is False

    def test_omnichannel_activity(self):
        oa = OmnichannelActivity.model_validate({
            "description": "Visited pricing",
            "actor": {"type": "user"},
            "source": {"type": "web"},
            "contact": {"id": 1},
        })
        assert oa.id is None
        assert oa.link is None

    def test_service_task(self):
        st = ServiceTask.model_validate({
            "id": 1, "status": 1, "type_id": 2, "ticket_id": 3,
            "created_at": TS, "updated_at": TS,
        })
        assert st.status == 1

    def test_field_technician(self):
        ft = FieldTechnician.model_validate({
            "id": 1, "name": "Bob", "email": "bob@co.com",
            "created_at": TS, "updated_at": TS,
        })
        assert ft.email == "bob@co.com"
