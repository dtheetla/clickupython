from typing import Optional, List, Any
from pydantic import BaseModel,  ValidationError, validator, Field


class Priority(BaseModel):
    priority: str
    color: str


class Status(BaseModel):
    status: str
    color: str
    hide_label: bool


class StatusElement(BaseModel):
    id: Optional[str]
    status: str
    orderindex: int
    color: str
    type: str


class Asssignee(BaseModel):
    id: str
    color: str
    username: str
    initials: str
    profilePicture: str


class ListFolder(BaseModel):
    id: str
    name: str
    hidden: Optional[bool]
    access: bool


class SingleList(BaseModel):
    id: str = None
    name: str = None
    deleted: bool = None
    archived: bool = None
    orderindex: int = None
    override_statuses: bool = None
    priority: Optional[Priority] = None
    assignee: Asssignee = None
    due_date: str = None
    start_date: None
    folder: ListFolder = None
    space: ListFolder = None
    statuses: Optional[List[StatusElement]] = None
    inbound_address: str = None
    permission_level: str = None
    content: Optional[str] = None
    status: Optional[Status] = None
    task_count: Optional[int] = None
    start_date_time: Optional[None] = None
    due_date_time: Optional[bool] = None

    # return a single list
    def build_list(self):
        return SingleList(**self)


class AllLists(BaseModel):
    lists: List[SingleList] = None

    # return a list of lists
    def build_lists(self):
        return AllLists(**self)


class ChecklistItem(BaseModel):
    id: str = None
    name: str = None
    orderindex: int = None
    assignee: Optional[Asssignee]


class Checklist(BaseModel):
    id: Optional[str]
    task_id: str = None
    name: str = None
    orderindex: int = None
    resolved: int = None
    unresolved: int = None
    items: List[ChecklistItem] = None

    def add_item(self, client_instance, name: str, assignee: str = None):
        return client_instance.create_checklist_item(self.id, name=name, assignee=assignee)


class Checklists(BaseModel):
    checklist: Checklist

    def build_checklist(self):
        final_checklist = Checklists(**self)
        return final_checklist.checklist


class Attachment(BaseModel):

    id: str
    version: int
    date: str
    title: str
    extension: str
    thumbnail_small: str
    thumbnail_large: str
    url: str

    def build_attachment(self):
        return Attachment(**self)


class User(BaseModel):
    id: str = None
    username: str = None
    initials: str = None
    email: str = None
    color: str = None
    profilePicture: str = None
    initials: Optional[str] = None
    role: Optional[int] = None
    custom_role: Optional[None] = None
    last_active: Optional[str] = None
    date_joined: Optional[str] = None
    date_invited: Optional[str] = None


class AssignedBy(BaseModel):
    id: str = None
    username: str = None
    initials: str = None
    email: str = None
    color: str = None
    profile_picture: str = None


class CommentComment(BaseModel):
    text: str = None


class Comment(BaseModel):
    id: str = None
    comment: List[CommentComment] = None
    comment_text: str = None
    user: AssignedBy = None
    resolved: bool = None
    assignee: AssignedBy = None
    assigned_by: AssignedBy = None
    reactions: List[Any] = None
    date: str = None

    def build_comment(self):
        return Comment(**self)


class Comments(BaseModel):
    comments: List[Comment] = None

    def __iter__(self):
        return iter(self.comments)

    def build_comments(self):
        return Comments(**self)


class Creator(BaseModel):
    id: int = None
    username: str = None
    color: str = None
    profile_picture: str = None


class TypeConfig(BaseModel):
    include_guests: Optional[bool]
    include_team_members: Optional[bool]


class CustomField(BaseModel):
    id: str
    name: str
    type: str
    type_config: TypeConfig
    date_created: str
    hide_from_guests: bool
    value: Optional[str]
    required: bool


class Space(BaseModel):
    id: int = None
    name: str = None
    access: bool = None


class Folder(BaseModel):
    id: str = None
    name: str = None
    orderindex: int = None
    override_statuses: bool = False
    hidden: bool = False
    space: Optional[Space] = None
    task_count: int = None
    lists: List[SingleList] = []

    def build_folder(self):
        return Folder(**self)

    def delete(self, client_instance):
        model = "folder/"
        deleted_folder_status = client_instance._delete_request(
            model, self.id)


class Folders(BaseModel):
    folders: List[Folder] = None

    def build_folders(self):
        return Folders(**self)


class Priority(BaseModel):
    id: int = None
    priority: str = None
    color: str = None
    orderindex: str = None


class Status(BaseModel):
    status: str
    color: str
    orderindex: int
    type: str


class ClickupList(BaseModel):
    id: str = None


# class Folder(BaseModel):
#     id: str = None


class Space(BaseModel):
    id: str = None


class Task(BaseModel):
    
    id: str = None
    custom_id: None = None
    name: str = None
    text_content: str = None
    description: str = None
    status: Status = None
    orderindex: str = None
    date_created: str = None
    date_updated: str = None
    date_closed: str = None
    creator: Creator = None
    task_assignees: List[Any] = Field(None, alias="assignees")
    task_checklists: List[Any] = Field(None, alias="checklists")
    task_tags: List[Any] = Field(None, alias="tags")
    parent: str = None
    priority: Optional[Priority]
    due_date: str = None
    start_date: str = None
    time_estimate: str = None
    time_spent: Optional[str] = None
    custom_fields: List[CustomField] = None
    list: ClickupList
    folder: Folder
    space: Folder
    url: str

    @validator('priority')
    def check_status(cls, v):

        if v == "":
            v = 4

            return v

    def build_task(self):
        return Task(**self)

    def delete(self):
        client.ClickUpClient.delete_task(self, self.id)

    def upload_attachment(self, client_instance, file_path: str):
        return client_instance.upload_attachment(self.id, file_path)

    def update(self, client_instance,  name: str = None, description: str = None, status: str = None, priority: int = None, time_estimate: int = None,
               archived: bool = None, add_assignees: List[str] = None, remove_assignees: List[int] = None):

        return client_instance.update_task(self.id, name, description, status, priority, time_estimate, archived, add_assignees, remove_assignees)

    def add_comment(self, client_instance, comment_text: str, assignee: str = None, notify_all: bool = True):
        return client_instance.create_task_comment(self.id, comment_text, assignee, notify_all)

    def get_comments(self, client_instance):
        return client_instance.get_task_comments(self.id)


class Tasks(BaseModel):
    tasks: List[Task] = None

    def __iter__(self):
        return iter(self.tasks)

    def build_tasks(self):
        return Tasks(**self)


class User(BaseModel):
    id: str = None
    username: str = None
    initials: str = None
    email: str = None
    color: str = None
    profilePicture: str = None
    initials: Optional[str] = None
    role: Optional[int] = None
    custom_role: Optional[None] = None
    last_active: Optional[str] = None
    date_joined: Optional[str] = None
    date_invited: Optional[str] = None


class InvitedBy(BaseModel):
    id: str = None
    username: str = None
    color: str = None
    email: str = None
    initials: str = None
    profile_picture: None = None


class Member(BaseModel):
    user: User
    invited_by: Optional[InvitedBy] = None


class Members(BaseModel):
    members: List[User] = None

    def __iter__(self):
        return iter(self.members)

    def build_members(self):
        return Members(**self)


class Team(BaseModel):
    id: str = None
    name: str = None
    color: str = None
    avatar: str = None
    members: List[Member] = None


class Teams(BaseModel):
    teams: List[Team] = None

    def __iter__(self):
        return iter(self.teams)

    def build_teams(self):
        return Teams(**self)


class Goal(BaseModel):
    id: str = None
    name: str = None
    team_id: int = None
    date_created: str = None
    start_date: str = None
    due_date: str = None
    description: str = None
    private: bool = None
    archived: bool = None
    creator: int = None
    color: str = None
    pretty_id: int = None
    multiple_owners: bool = None
    folder_id: str = None
    members: List[User] = None
    owners: List[User] = None
    key_results: List[Any] = None
    percent_completed: int = None
    history: List[Any] = None
    pretty_url: str = None

    def build_goal(self):
        return Goal(**self)


class Goals(BaseModel):
    goal: Goal

    def build_goals(self):
        built_goal = Goals(**self)
        return built_goal.goal


class GoalsList(BaseModel):
    goals: List[Goal] = None

    def __iter__(self):
        return iter(self.goals)

    def build_goals(self):
        return GoalsList(**self)
