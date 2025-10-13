import { useState, useEffect } from "react";
import axios from "axios";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "../components/ui/avatar";
import { Badge } from "../components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { toast } from "sonner";
import { LogOut, BookOpen, Calendar, ClipboardList, Library, MessageSquare, TrendingUp, Download, ThumbsUp } from "lucide-react";
import { Progress } from "../components/ui/progress";
import { Separator } from "../components/ui/separator";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "../components/ui/dialog";
import { Textarea } from "../components/ui/textarea";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const StudentDashboard = ({ user, onLogout }) => {
  const [grades, setGrades] = useState([]);
  const [attendance, setAttendance] = useState([]);
  const [materials, setMaterials] = useState([]);
  const [library, setLibrary] = useState([]);
  const [events, setEvents] = useState([]);
  const [complaints, setComplaints] = useState([]);
  const [notices, setNotices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showComplaintDialog, setShowComplaintDialog] = useState(false);
  const [newComplaint, setNewComplaint] = useState({ title: "", description: "", type: "public" });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [gradesRes, attendanceRes, materialsRes, libraryRes, eventsRes, complaintsRes, noticesRes] = await Promise.all([
        axios.get(`${API}/grades/${user.id}`),
        axios.get(`${API}/attendance/${user.id}`),
        axios.get(`${API}/materials`),
        axios.get(`${API}/library`),
        axios.get(`${API}/events`),
        axios.get(`${API}/complaints`),
        axios.get(`${API}/notices`),
      ]);

      setGrades(gradesRes.data);
      setAttendance(attendanceRes.data);
      setMaterials(materialsRes.data);
      setLibrary(libraryRes.data);
      setEvents(eventsRes.data);
      setComplaints(complaintsRes.data);
      setNotices(noticesRes.data.filter(n => n.target_audience.includes("student") || n.target_audience.includes("all")));
    } catch (error) {
      console.error("Error fetching data:", error);
      toast.error("Failed to load data");
    } finally {
      setLoading(false);
    }
  };

  const handleRegisterEvent = async (eventId) => {
    try {
      await axios.post(`${API}/events/${eventId}/register`, { user_id: user.id });
      toast.success("Registered for event successfully!");
      fetchData();
    } catch (error) {
      console.error("Error registering for event:", error);
      toast.error("Failed to register for event");
    }
  };

  const handleVoteComplaint = async (complaintId) => {
    try {
      const response = await axios.post(`${API}/complaints/${complaintId}/vote`, { user_id: user.id });
      toast.success(response.data.message);
      fetchData();
    } catch (error) {
      console.error("Error voting:", error);
      toast.error("Failed to vote");
    }
  };

  const handleSubmitComplaint = async () => {
    if (!newComplaint.title || !newComplaint.description) {
      toast.error("Please fill all fields");
      return;
    }

    try {
      const complaint = {
        id: `C${Date.now()}`,
        title: newComplaint.title,
        description: newComplaint.description,
        complaint_type: newComplaint.type,
        status: "pending",
        submitted_by: user.id,
        submitted_by_name: user.name,
        submitted_date: new Date().toISOString().split('T')[0],
        votes: 0,
        voted_by: [],
      };

      await axios.post(`${API}/complaints`, complaint);
      toast.success("Complaint submitted successfully!");
      setShowComplaintDialog(false);
      setNewComplaint({ title: "", description: "", type: "public" });
      fetchData();
    } catch (error) {
      console.error("Error submitting complaint:", error);
      toast.error("Failed to submit complaint");
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

  const avgAttendance = attendance.length > 0 
    ? (attendance.reduce((sum, a) => sum + a.percentage, 0) / attendance.length).toFixed(2)
    : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
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
              <p className="text-sm text-gray-500">Student ID: {user.id}</p>
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
        <div className="mb-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card data-testid="summary-card-grades" className="card-hover">
            <CardHeader className="pb-3">
              <CardDescription>Average Grade</CardDescription>
              <CardTitle className="text-3xl">
                {grades.length > 0 ? grades[0].grade : "N/A"}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">{grades.length} subjects</p>
            </CardContent>
          </Card>

          <Card data-testid="summary-card-attendance" className="card-hover">
            <CardHeader className="pb-3">
              <CardDescription>Average Attendance</CardDescription>
              <CardTitle className="text-3xl">{avgAttendance}%</CardTitle>
            </CardHeader>
            <CardContent>
              <Progress value={avgAttendance} className="h-2" />
            </CardContent>
          </Card>

          <Card data-testid="summary-card-events" className="card-hover">
            <CardHeader className="pb-3">
              <CardDescription>Upcoming Events</CardDescription>
              <CardTitle className="text-3xl">{events.filter(e => new Date(e.date) >= new Date()).length}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">Register now</p>
            </CardContent>
          </Card>
        </div>

        {/* Notices */}
        {notices.length > 0 && (
          <Card data-testid="notices-section" className="mb-8">
            <CardHeader>
              <CardTitle>Important Notices</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {notices.map((notice) => (
                <div key={notice.id} data-testid={`notice-${notice.id}`} className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <div className="flex items-start justify-between">
                    <div>
                      <h4 className="font-semibold text-sm">{notice.title}</h4>
                      <p className="text-sm text-gray-600 mt-1">{notice.content}</p>
                    </div>
                    <Badge variant={notice.priority === "high" ? "destructive" : "secondary"}>
                      {notice.priority}
                    </Badge>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        )}

        {/* Tabs */}
        <Tabs defaultValue="grades" className="space-y-6">
          <TabsList data-testid="dashboard-tabs" className="grid grid-cols-3 lg:grid-cols-6 w-full">
            <TabsTrigger value="grades" data-testid="tab-grades">
              <TrendingUp className="w-4 h-4 mr-2" />
              Grades
            </TabsTrigger>
            <TabsTrigger value="attendance" data-testid="tab-attendance">
              <ClipboardList className="w-4 h-4 mr-2" />
              Attendance
            </TabsTrigger>
            <TabsTrigger value="materials" data-testid="tab-materials">
              <BookOpen className="w-4 h-4 mr-2" />
              Materials
            </TabsTrigger>
            <TabsTrigger value="library" data-testid="tab-library">
              <Library className="w-4 h-4 mr-2" />
              Library
            </TabsTrigger>
            <TabsTrigger value="events" data-testid="tab-events">
              <Calendar className="w-4 h-4 mr-2" />
              Events
            </TabsTrigger>
            <TabsTrigger value="complaints" data-testid="tab-complaints">
              <MessageSquare className="w-4 h-4 mr-2" />
              Complaints
            </TabsTrigger>
          </TabsList>

          {/* Grades Tab */}
          <TabsContent value="grades" data-testid="grades-content">
            <Card>
              <CardHeader>
                <CardTitle>Academic Performance</CardTitle>
                <CardDescription>Anna University Exam Pattern (Part A: 5×2=10, Part B: 5×8=40)</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {grades.map((grade) => (
                    <div key={grade.id} data-testid={`grade-${grade.id}`} className="p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <div>
                          <h4 className="font-semibold">{grade.subject}</h4>
                          <p className="text-sm text-gray-500">{grade.subject_code}</p>
                        </div>
                        <Badge className="text-lg px-4 py-1">{grade.grade}</Badge>
                      </div>
                      <Separator className="my-2" />
                      <div className="grid grid-cols-3 gap-4 text-sm">
                        <div>
                          <p className="text-gray-500">Part A (10)</p>
                          <p className="font-semibold" data-testid={`grade-${grade.id}-part-a`}>{grade.part_a_marks}</p>
                        </div>
                        <div>
                          <p className="text-gray-500">Part B (40)</p>
                          <p className="font-semibold" data-testid={`grade-${grade.id}-part-b`}>{grade.part_b_marks}</p>
                        </div>
                        <div>
                          <p className="text-gray-500">Total (50)</p>
                          <p className="font-semibold text-lg" data-testid={`grade-${grade.id}-total`}>{grade.total_marks}</p>
                        </div>
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
                <CardTitle>Attendance Records</CardTitle>
                <CardDescription>Track your class attendance</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {attendance.map((att) => (
                    <div key={att.id} data-testid={`attendance-${att.id}`} className="p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-center justify-between mb-3">
                        <div>
                          <h4 className="font-semibold">{att.subject}</h4>
                          <p className="text-sm text-gray-500">{att.subject_code}</p>
                        </div>
                        <Badge variant={att.percentage >= 75 ? "default" : "destructive"}>
                          {att.percentage.toFixed(1)}%
                        </Badge>
                      </div>
                      <Progress value={att.percentage} className="h-2 mb-2" />
                      <p className="text-sm text-gray-600">
                        {att.attended_classes} / {att.total_classes} classes attended
                      </p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Study Materials Tab */}
          <TabsContent value="materials" data-testid="materials-content">
            <Card>
              <CardHeader>
                <CardTitle>Study Materials</CardTitle>
                <CardDescription>Download lecture notes and study resources</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {materials.map((material) => (
                    <div key={material.id} data-testid={`material-${material.id}`} className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h4 className="font-semibold">{material.title}</h4>
                          <p className="text-sm text-gray-500 mt-1">{material.subject} ({material.subject_code})</p>
                          <p className="text-sm text-gray-600 mt-2">{material.description}</p>
                          <p className="text-xs text-gray-400 mt-2">
                            Uploaded by {material.uploaded_by} on {material.uploaded_date}
                          </p>
                        </div>
                        <Button data-testid={`download-material-${material.id}`} size="sm" variant="outline">
                          <Download className="w-4 h-4 mr-2" />
                          Download
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Library Tab */}
          <TabsContent value="library" data-testid="library-content">
            <Card>
              <CardHeader>
                <CardTitle>Online Library</CardTitle>
                <CardDescription>Browse available books</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {library.map((book) => (
                    <div key={book.id} data-testid={`book-${book.id}`} className="p-4 bg-gray-50 rounded-lg">
                      <h4 className="font-semibold">{book.title}</h4>
                      <p className="text-sm text-gray-500 mt-1">by {book.author}</p>
                      <p className="text-xs text-gray-400 mt-2">ISBN: {book.isbn}</p>
                      <div className="flex items-center justify-between mt-3">
                        <Badge variant={book.available ? "default" : "secondary"}>
                          {book.available ? "Available" : "Not Available"}
                        </Badge>
                        <span className="text-sm text-gray-600">
                          {book.available_copies} / {book.total_copies} copies
                        </span>
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
                <CardTitle>Academic Calendar & Events</CardTitle>
                <CardDescription>Register for upcoming events</CardDescription>
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
                        {event.registration_required && event.event_type !== "holiday" && (
                          <Button
                            data-testid={`register-event-${event.id}`}
                            size="sm"
                            onClick={() => handleRegisterEvent(event.id)}
                            disabled={event.registered_users.includes(user.id)}
                          >
                            {event.registered_users.includes(user.id) ? "Registered" : "Register"}
                          </Button>
                        )}
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
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Complaints & Feedback</CardTitle>
                    <CardDescription>Submit and vote on campus issues</CardDescription>
                  </div>
                  <Button data-testid="submit-complaint-btn" onClick={() => setShowComplaintDialog(true)}>
                    Submit Complaint
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {complaints
                    .filter((c) => c.complaint_type === "public" || c.submitted_by === user.id)
                    .map((complaint) => (
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
                            {complaint.response && (
                              <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded">
                                <p className="text-sm font-semibold text-green-800">Response:</p>
                                <p className="text-sm text-green-700">{complaint.response}</p>
                              </div>
                            )}
                          </div>
                        </div>
                        {complaint.complaint_type === "public" && (
                          <div className="flex items-center gap-2 mt-3">
                            <Button
                              data-testid={`vote-complaint-${complaint.id}`}
                              size="sm"
                              variant={complaint.voted_by.includes(user.id) ? "default" : "outline"}
                              onClick={() => handleVoteComplaint(complaint.id)}
                            >
                              <ThumbsUp className="w-4 h-4 mr-2" />
                              {complaint.votes} votes
                            </Button>
                          </div>
                        )}
                      </div>
                    ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>

      {/* Submit Complaint Dialog */}
      <Dialog open={showComplaintDialog} onOpenChange={setShowComplaintDialog}>
        <DialogContent data-testid="complaint-dialog">
          <DialogHeader>
            <DialogTitle>Submit a Complaint</DialogTitle>
            <DialogDescription>Let us know about any issues or suggestions</DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="complaint-title">Title</Label>
              <Input
                data-testid="complaint-title-input"
                id="complaint-title"
                value={newComplaint.title}
                onChange={(e) => setNewComplaint({ ...newComplaint, title: e.target.value })}
                placeholder="Brief title for your complaint"
              />
            </div>
            <div>
              <Label htmlFor="complaint-description">Description</Label>
              <Textarea
                data-testid="complaint-description-input"
                id="complaint-description"
                value={newComplaint.description}
                onChange={(e) => setNewComplaint({ ...newComplaint, description: e.target.value })}
                placeholder="Detailed description of the issue"
                rows={4}
              />
            </div>
            <div>
              <Label htmlFor="complaint-type">Type</Label>
              <Select
                value={newComplaint.type}
                onValueChange={(value) => setNewComplaint({ ...newComplaint, type: value })}
              >
                <SelectTrigger data-testid="complaint-type-select">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="public">Public (visible to all, can be voted)</SelectItem>
                  <SelectItem value="private">Private (only admins can see)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button data-testid="submit-complaint-confirm-btn" onClick={handleSubmitComplaint} className="w-full">
              Submit Complaint
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default StudentDashboard;