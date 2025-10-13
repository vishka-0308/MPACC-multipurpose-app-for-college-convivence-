import { useState, useEffect } from "react";
import axios from "axios";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "../components/ui/avatar";
import { Badge } from "../components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { toast } from "sonner";
import { LogOut, Calendar, Users, MessageSquare, Bell, UserPlus, Edit, Trash2 } from "lucide-react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "../components/ui/dialog";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { Textarea } from "../components/ui/textarea";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminDashboard = ({ user, onLogout }) => {
  const [users, setUsers] = useState([]);
  const [students, setStudents] = useState([]);
  const [events, setEvents] = useState([]);
  const [complaints, setComplaints] = useState([]);
  const [notices, setNotices] = useState([]);
  const [attendance, setAttendance] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showEventDialog, setShowEventDialog] = useState(false);
  const [showNoticeDialog, setShowNoticeDialog] = useState(false);
  const [showUserDialog, setShowUserDialog] = useState(false);
  const [showWaiverDialog, setShowWaiverDialog] = useState(false);
  
  const [eventForm, setEventForm] = useState({
    title: "", description: "", date: "", time: "", location: "", event_type: "academic", registration_required: true
  });
  
  const [noticeForm, setNoticeForm] = useState({
    title: "", content: "", priority: "medium", target_audience: ["all"]
  });
  
  const [userForm, setUserForm] = useState({
    id: "", username: "", password: "", role: "student", name: "", email: ""
  });

  const [waiverForm, setWaiverForm] = useState({
    student_id: "", subject_code: "", reason: ""
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [usersRes, studentsRes, eventsRes, complaintsRes, noticesRes, attendanceRes] = await Promise.all([
        axios.get(`${API}/users`),
        axios.get(`${API}/students`),
        axios.get(`${API}/events`),
        axios.get(`${API}/complaints`),
        axios.get(`${API}/notices`),
        axios.get(`${API}/attendance`),
      ]);

      setUsers(usersRes.data);
      setStudents(studentsRes.data);
      setEvents(eventsRes.data);
      setComplaints(complaintsRes.data);
      setNotices(noticesRes.data);
      setAttendance(attendanceRes.data);
    } catch (error) {
      console.error("Error fetching data:", error);
      toast.error("Failed to load data");
    } finally {
      setLoading(false);
    }
  };

  const handleCreateEvent = async () => {
    if (!eventForm.title || !eventForm.date) {
      toast.error("Please fill required fields");
      return;
    }

    try {
      const event = {
        id: `E${Date.now()}`,
        ...eventForm,
        registered_users: []
      };

      await axios.post(`${API}/events`, event);
      toast.success("Event created successfully!");
      setShowEventDialog(false);
      setEventForm({ title: "", description: "", date: "", time: "", location: "", event_type: "academic", registration_required: true });
      fetchData();
    } catch (error) {
      console.error("Error creating event:", error);
      toast.error("Failed to create event");
    }
  };

  const handleCreateNotice = async () => {
    if (!noticeForm.title || !noticeForm.content) {
      toast.error("Please fill required fields");
      return;
    }

    try {
      const notice = {
        id: `N${Date.now()}`,
        ...noticeForm,
        posted_by: user.name,
        posted_date: new Date().toISOString().split('T')[0]
      };

      await axios.post(`${API}/notices`, notice);
      toast.success("Notice posted successfully!");
      setShowNoticeDialog(false);
      setNoticeForm({ title: "", content: "", priority: "medium", target_audience: ["all"] });
      fetchData();
    } catch (error) {
      console.error("Error creating notice:", error);
      toast.error("Failed to post notice");
    }
  };

  const handleCreateUser = async () => {
    if (!userForm.id || !userForm.username || !userForm.password || !userForm.name || !userForm.email) {
      toast.error("Please fill all fields");
      return;
    }

    try {
      const newUser = {
        ...userForm,
        profile_pic: `https://api.dicebear.com/7.x/avataaars/svg?seed=${userForm.name}`
      };

      await axios.post(`${API}/users`, newUser);
      toast.success("User created successfully!");
      setShowUserDialog(false);
      setUserForm({ id: "", username: "", password: "", role: "student", name: "", email: "" });
      fetchData();
    } catch (error) {
      console.error("Error creating user:", error);
      toast.error("Failed to create user");
    }
  };

  const handleDeleteUser = async (userId) => {
    if (!window.confirm("Are you sure you want to delete this user?")) return;

    try {
      await axios.delete(`${API}/users/${userId}`);
      toast.success("User deleted successfully!");
      fetchData();
    } catch (error) {
      console.error("Error deleting user:", error);
      toast.error("Failed to delete user");
    }
  };

  const handleDeleteNotice = async (noticeId) => {
    try {
      await axios.delete(`${API}/notices/${noticeId}`);
      toast.success("Notice deleted successfully!");
      fetchData();
    } catch (error) {
      console.error("Error deleting notice:", error);
      toast.error("Failed to delete notice");
    }
  };

  const handleResolveComplaint = async (complaintId) => {
    const response = prompt("Enter your response to resolve this complaint:");
    if (!response) return;

    try {
      await axios.put(`${API}/complaints/${complaintId}/resolve`, { response });
      toast.success("Complaint resolved!");
      fetchData();
    } catch (error) {
      console.error("Error resolving complaint:", error);
      toast.error("Failed to resolve complaint");
    }
  };

  const handleWaiveAttendance = async () => {
    if (!waiverForm.student_id || !waiverForm.subject_code || !waiverForm.reason) {
      toast.error("Please fill all fields");
      return;
    }

    try {
      await axios.post(`${API}/attendance/waive`, waiverForm);
      toast.success("Attendance waived successfully!");
      setShowWaiverDialog(false);
      setWaiverForm({ student_id: "", subject_code: "", reason: "" });
      fetchData();
    } catch (error) {
      console.error("Error waiving attendance:", error);
      toast.error("Failed to waive attendance");
    }
  };

  const resetDemoData = async () => {
    try {
      await axios.post(`${API}/reset-demo-data`);
      toast.success("Demo data reset successfully!");
      fetchData();
    } catch (error) {
      console.error("Error resetting data:", error);
      toast.error("Failed to reset data");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-50 shadow-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Avatar className="w-12 h-12">
              <AvatarImage src={user.profile_pic} alt={user.name} />
              <AvatarFallback>{user.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
            </Avatar>
            <div>
              <h2 className="font-semibold text-lg" data-testid="user-name">{user.name}</h2>
              <p className="text-sm text-gray-500">Administrator</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Button data-testid="reset-demo-btn" variant="outline" size="sm" onClick={resetDemoData}>
              Reset Demo Data
            </Button>
            <Button data-testid="logout-btn" variant="ghost" size="sm" onClick={onLogout}>
              <LogOut className="w-4 h-4 mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Dashboard Summary */}
        <div className="mb-8 grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card data-testid="summary-card-users" className="card-hover">
            <CardHeader className="pb-3">
              <CardDescription>Total Users</CardDescription>
              <CardTitle className="text-3xl">{users.length}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">
                {users.filter(u => u.role === "student").length} students, {users.filter(u => u.role === "teacher").length} teachers
              </p>
            </CardContent>
          </Card>

          <Card data-testid="summary-card-events" className="card-hover">
            <CardHeader className="pb-3">
              <CardDescription>Total Events</CardDescription>
              <CardTitle className="text-3xl">{events.length}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">Academic & Cultural</p>
            </CardContent>
          </Card>

          <Card data-testid="summary-card-complaints" className="card-hover">
            <CardHeader className="pb-3">
              <CardDescription>Pending Complaints</CardDescription>
              <CardTitle className="text-3xl">{complaints.filter(c => c.status === "pending").length}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">Need attention</p>
            </CardContent>
          </Card>

          <Card data-testid="summary-card-notices" className="card-hover">
            <CardHeader className="pb-3">
              <CardDescription>Active Notices</CardDescription>
              <CardTitle className="text-3xl">{notices.length}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">Posted announcements</p>
            </CardContent>
          </Card>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="users" className="space-y-6">
          <TabsList data-testid="dashboard-tabs" className="grid grid-cols-2 lg:grid-cols-5 w-full">
            <TabsTrigger value="users" data-testid="tab-users">
              <Users className="w-4 h-4 mr-2" />
              Users
            </TabsTrigger>
            <TabsTrigger value="events" data-testid="tab-events">
              <Calendar className="w-4 h-4 mr-2" />
              Events
            </TabsTrigger>
            <TabsTrigger value="complaints" data-testid="tab-complaints">
              <MessageSquare className="w-4 h-4 mr-2" />
              Complaints
            </TabsTrigger>
            <TabsTrigger value="notices" data-testid="tab-notices">
              <Bell className="w-4 h-4 mr-2" />
              Notices
            </TabsTrigger>
            <TabsTrigger value="attendance" data-testid="tab-attendance">
              <UserPlus className="w-4 h-4 mr-2" />
              Attendance
            </TabsTrigger>
          </TabsList>

          {/* Users Tab */}
          <TabsContent value="users" data-testid="users-content">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>User Management</CardTitle>
                    <CardDescription>Manage student, teacher, and admin accounts</CardDescription>
                  </div>
                  <Button data-testid="add-user-btn" onClick={() => setShowUserDialog(true)}>
                    <UserPlus className="w-4 h-4 mr-2" />
                    Add User
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {users.map((u) => (
                    <div key={u.id} data-testid={`user-${u.id}`} className="p-4 bg-gray-50 rounded-lg flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <Avatar>
                          <AvatarImage src={u.profile_pic} alt={u.name} />
                          <AvatarFallback>{u.name[0]}</AvatarFallback>
                        </Avatar>
                        <div>
                          <h4 className="font-semibold">{u.name}</h4>
                          <p className="text-sm text-gray-500">{u.email} • ID: {u.id}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge>{u.role}</Badge>
                        <Button data-testid={`delete-user-${u.id}`} size="sm" variant="destructive" onClick={() => handleDeleteUser(u.id)}>
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Events Tab */}
          <TabsContent value="events" data-testid="events-content">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Event Management</CardTitle>
                    <CardDescription>Create and manage campus events</CardDescription>
                  </div>
                  <Button data-testid="create-event-btn" onClick={() => setShowEventDialog(true)}>
                    Create Event
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {events.map((event) => (
                    <div key={event.id} data-testid={`event-${event.id}`} className="p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <h4 className="font-semibold">{event.title}</h4>
                            <Badge variant={event.event_type === "holiday" ? "secondary" : "default"}>
                              {event.event_type}
                            </Badge>
                          </div>
                          <p className="text-sm text-gray-600 mb-2">{event.description}</p>
                          <div className="flex items-center gap-4 text-sm text-gray-500">
                            <span>📅 {event.date}</span>
                            <span>⏰ {event.time}</span>
                            <span>📍 {event.location}</span>
                          </div>
                          {event.registered_users.length > 0 && (
                            <p className="text-xs text-gray-400 mt-2">
                              {event.registered_users.length} registered
                            </p>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Complaints Tab */}
          <TabsContent value="complaints" data-testid="complaints-content">
            <Card>
              <CardHeader>
                <CardTitle>Complaint Management</CardTitle>
                <CardDescription>Monitor and resolve student complaints</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {complaints.map((complaint) => (
                    <div key={complaint.id} data-testid={`complaint-${complaint.id}`} className="p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <h4 className="font-semibold">{complaint.title}</h4>
                            <Badge variant={complaint.status === "resolved" ? "default" : "secondary"}>
                              {complaint.status}
                            </Badge>
                            <Badge variant="outline">{complaint.complaint_type}</Badge>
                          </div>
                          <p className="text-sm text-gray-600 mb-2">{complaint.description}</p>
                          <p className="text-xs text-gray-400">
                            Submitted by {complaint.submitted_by_name} on {complaint.submitted_date}
                          </p>
                          {complaint.complaint_type === "public" && (
                            <p className="text-xs text-gray-500 mt-1">{complaint.votes} votes</p>
                          )}
                          {complaint.response && (
                            <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded">
                              <p className="text-sm font-semibold text-green-800">Response:</p>
                              <p className="text-sm text-green-700">{complaint.response}</p>
                            </div>
                          )}
                        </div>
                      </div>
                      {complaint.status === "pending" && (
                        <div className="mt-3">
                          <Button data-testid={`resolve-complaint-${complaint.id}`} size="sm" onClick={() => handleResolveComplaint(complaint.id)}>
                            Resolve Complaint
                          </Button>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Notices Tab */}
          <TabsContent value="notices" data-testid="notices-content">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Notice Board</CardTitle>
                    <CardDescription>Post and manage announcements</CardDescription>
                  </div>
                  <Button data-testid="post-notice-btn" onClick={() => setShowNoticeDialog(true)}>
                    Post Notice
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {notices.map((notice) => (
                    <div key={notice.id} data-testid={`notice-${notice.id}`} className="p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <h4 className="font-semibold">{notice.title}</h4>
                            <Badge variant={notice.priority === "high" ? "destructive" : "secondary"}>
                              {notice.priority}
                            </Badge>
                          </div>
                          <p className="text-sm text-gray-600 mb-2">{notice.content}</p>
                          <p className="text-xs text-gray-400">
                            Posted by {notice.posted_by} on {notice.posted_date} • Target: {notice.target_audience.join(", ")}
                          </p>
                        </div>
                        <Button data-testid={`delete-notice-${notice.id}`} size="sm" variant="ghost" onClick={() => handleDeleteNotice(notice.id)}>
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Attendance Tab */}
          <TabsContent value="attendance" data-testid="attendance-content">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Attendance Waiver</CardTitle>
                    <CardDescription>Waive attendance for valid reasons</CardDescription>
                  </div>
                  <Button data-testid="waive-attendance-btn" onClick={() => setShowWaiverDialog(true)}>
                    Waive Attendance
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {attendance.map((att) => (
                    <div key={att.id} data-testid={`attendance-${att.id}`} className="p-3 bg-gray-50 rounded-lg flex items-center justify-between">
                      <div>
                        <h4 className="font-medium">{att.student_name}</h4>
                        <p className="text-sm text-gray-500">
                          {att.subject} ({att.subject_code}) - {att.percentage.toFixed(1)}%
                        </p>
                      </div>
                      <Badge variant={att.percentage >= 75 ? "default" : "destructive"}>
                        {att.attended_classes}/{att.total_classes}
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>

      {/* Create Event Dialog */}
      <Dialog open={showEventDialog} onOpenChange={setShowEventDialog}>
        <DialogContent data-testid="event-dialog">
          <DialogHeader>
            <DialogTitle>Create New Event</DialogTitle>
            <DialogDescription>Add a new event to the academic calendar</DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="event-title">Title</Label>
              <Input
                data-testid="event-title-input"
                id="event-title"
                value={eventForm.title}
                onChange={(e) => setEventForm({ ...eventForm, title: e.target.value })}
              />
            </div>
            <div>
              <Label htmlFor="event-description">Description</Label>
              <Textarea
                data-testid="event-description-input"
                id="event-description"
                value={eventForm.description}
                onChange={(e) => setEventForm({ ...eventForm, description: e.target.value })}
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="event-date">Date</Label>
                <Input
                  data-testid="event-date-input"
                  id="event-date"
                  type="date"
                  value={eventForm.date}
                  onChange={(e) => setEventForm({ ...eventForm, date: e.target.value })}
                />
              </div>
              <div>
                <Label htmlFor="event-time">Time</Label>
                <Input
                  data-testid="event-time-input"
                  id="event-time"
                  value={eventForm.time}
                  onChange={(e) => setEventForm({ ...eventForm, time: e.target.value })}
                />
              </div>
            </div>
            <div>
              <Label htmlFor="event-location">Location</Label>
              <Input
                data-testid="event-location-input"
                id="event-location"
                value={eventForm.location}
                onChange={(e) => setEventForm({ ...eventForm, location: e.target.value })}
              />
            </div>
            <div>
              <Label htmlFor="event-type">Event Type</Label>
              <Select
                value={eventForm.event_type}
                onValueChange={(value) => setEventForm({ ...eventForm, event_type: value })}
              >
                <SelectTrigger data-testid="event-type-select">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="academic">Academic</SelectItem>
                  <SelectItem value="cultural">Cultural</SelectItem>
                  <SelectItem value="sports">Sports</SelectItem>
                  <SelectItem value="holiday">Holiday</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button data-testid="create-event-confirm-btn" onClick={handleCreateEvent} className="w-full">
              Create Event
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* Post Notice Dialog */}
      <Dialog open={showNoticeDialog} onOpenChange={setShowNoticeDialog}>
        <DialogContent data-testid="notice-dialog">
          <DialogHeader>
            <DialogTitle>Post New Notice</DialogTitle>
            <DialogDescription>Create an announcement for students and teachers</DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="notice-title">Title</Label>
              <Input
                data-testid="notice-title-input"
                id="notice-title"
                value={noticeForm.title}
                onChange={(e) => setNoticeForm({ ...noticeForm, title: e.target.value })}
              />
            </div>
            <div>
              <Label htmlFor="notice-content">Content</Label>
              <Textarea
                data-testid="notice-content-input"
                id="notice-content"
                value={noticeForm.content}
                onChange={(e) => setNoticeForm({ ...noticeForm, content: e.target.value })}
                rows={4}
              />
            </div>
            <div>
              <Label htmlFor="notice-priority">Priority</Label>
              <Select
                value={noticeForm.priority}
                onValueChange={(value) => setNoticeForm({ ...noticeForm, priority: value })}
              >
                <SelectTrigger data-testid="notice-priority-select">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="low">Low</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button data-testid="post-notice-confirm-btn" onClick={handleCreateNotice} className="w-full">
              Post Notice
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* Add User Dialog */}
      <Dialog open={showUserDialog} onOpenChange={setShowUserDialog}>
        <DialogContent data-testid="user-dialog">
          <DialogHeader>
            <DialogTitle>Add New User</DialogTitle>
            <DialogDescription>Create a student, teacher, or admin account</DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="user-id">User ID</Label>
                <Input
                  data-testid="user-id-input"
                  id="user-id"
                  value={userForm.id}
                  onChange={(e) => setUserForm({ ...userForm, id: e.target.value })}
                  placeholder="S128 / T204 / A002"
                />
              </div>
              <div>
                <Label htmlFor="user-role">Role</Label>
                <Select
                  value={userForm.role}
                  onValueChange={(value) => setUserForm({ ...userForm, role: value })}
                >
                  <SelectTrigger data-testid="user-role-select">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="student">Student</SelectItem>
                    <SelectItem value="teacher">Teacher</SelectItem>
                    <SelectItem value="admin">Admin</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div>
              <Label htmlFor="user-name">Full Name</Label>
              <Input
                data-testid="user-name-input"
                id="user-name"
                value={userForm.name}
                onChange={(e) => setUserForm({ ...userForm, name: e.target.value })}
              />
            </div>
            <div>
              <Label htmlFor="user-email">Email</Label>
              <Input
                data-testid="user-email-input"
                id="user-email"
                type="email"
                value={userForm.email}
                onChange={(e) => setUserForm({ ...userForm, email: e.target.value })}
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="user-username">Username</Label>
                <Input
                  data-testid="user-username-input"
                  id="user-username"
                  value={userForm.username}
                  onChange={(e) => setUserForm({ ...userForm, username: e.target.value })}
                />
              </div>
              <div>
                <Label htmlFor="user-password">Password</Label>
                <Input
                  data-testid="user-password-input"
                  id="user-password"
                  type="password"
                  value={userForm.password}
                  onChange={(e) => setUserForm({ ...userForm, password: e.target.value })}
                />
              </div>
            </div>
            <Button data-testid="create-user-confirm-btn" onClick={handleCreateUser} className="w-full">
              Create User
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* Waive Attendance Dialog */}
      <Dialog open={showWaiverDialog} onOpenChange={setShowWaiverDialog}>
        <DialogContent data-testid="waiver-dialog">
          <DialogHeader>
            <DialogTitle>Waive Attendance</DialogTitle>
            <DialogDescription>Set attendance to 100% for a student in a subject</DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="waiver-student">Student ID</Label>
              <Select
                value={waiverForm.student_id}
                onValueChange={(value) => setWaiverForm({ ...waiverForm, student_id: value })}
              >
                <SelectTrigger data-testid="waiver-student-select">
                  <SelectValue placeholder="Select student" />
                </SelectTrigger>
                <SelectContent>
                  {students.map((student) => (
                    <SelectItem key={student.id} value={student.id}>
                      {student.name} ({student.id})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="waiver-subject">Subject Code</Label>
              <Input
                data-testid="waiver-subject-input"
                id="waiver-subject"
                value={waiverForm.subject_code}
                onChange={(e) => setWaiverForm({ ...waiverForm, subject_code: e.target.value })}
                placeholder="CS301"
              />
            </div>
            <div>
              <Label htmlFor="waiver-reason">Reason</Label>
              <Textarea
                data-testid="waiver-reason-input"
                id="waiver-reason"
                value={waiverForm.reason}
                onChange={(e) => setWaiverForm({ ...waiverForm, reason: e.target.value })}
                placeholder="Medical reasons, sports participation, etc."
                rows={3}
              />
            </div>
            <Button data-testid="waive-attendance-confirm-btn" onClick={handleWaiveAttendance} className="w-full">
              Waive Attendance
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default AdminDashboard;
