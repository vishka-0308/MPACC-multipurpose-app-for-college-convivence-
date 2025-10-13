import { useState, useEffect } from "react";
import axios from "axios";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "../components/ui/avatar";
import { Badge } from "../components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { toast } from "sonner";
import { LogOut, BookOpen, Calendar, ClipboardList, MessageSquare, Edit } from "lucide-react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "../components/ui/dialog";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { Separator } from "../components/ui/separator";
import { Textarea } from "../components/ui/textarea";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const TeacherDashboard = ({ user, onLogout }) => {
  const [grades, setGrades] = useState([]);
  const [schedules, setSchedules] = useState([]);
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showGradeDialog, setShowGradeDialog] = useState(false);
  const [editingGrade, setEditingGrade] = useState(null);
  const [gradeForm, setGradeForm] = useState({
    part_a_marks: 0,
    part_b_marks: 0,
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [gradesRes, schedulesRes, complaintsRes] = await Promise.all([
        axios.get(`${API}/grades`),
        axios.get(`${API}/schedules/teacher/${user.id}`),
        axios.get(`${API}/complaints`),
      ]);

      setGrades(gradesRes.data);
      setSchedules(schedulesRes.data);
      setComplaints(complaintsRes.data.filter(c => c.status === "pending"));
    } catch (error) {
      console.error("Error fetching data:", error);
      toast.error("Failed to load data");
    } finally {
      setLoading(false);
    }
  };

  const calculateGrade = (total) => {
    if (total >= 45) return "A+";
    if (total >= 40) return "A";
    if (total >= 35) return "B+";
    if (total >= 30) return "B";
    if (total >= 25) return "C";
    return "F";
  };

  const handleEditGrade = (grade) => {
    setEditingGrade(grade);
    setGradeForm({
      part_a_marks: grade.part_a_marks,
      part_b_marks: grade.part_b_marks,
    });
    setShowGradeDialog(true);
  };

  const handleUpdateGrade = async () => {
    if (gradeForm.part_a_marks < 0 || gradeForm.part_a_marks > 10) {
      toast.error("Part A marks must be between 0 and 10");
      return;
    }
    if (gradeForm.part_b_marks < 0 || gradeForm.part_b_marks > 40) {
      toast.error("Part B marks must be between 0 and 40");
      return;
    }

    try {
      const total = parseInt(gradeForm.part_a_marks) + parseInt(gradeForm.part_b_marks);
      const grade = calculateGrade(total);

      const updatedGrade = {
        ...editingGrade,
        part_a_marks: parseInt(gradeForm.part_a_marks),
        part_b_marks: parseInt(gradeForm.part_b_marks),
        total_marks: total,
        grade: grade,
      };

      await axios.put(`${API}/grades/${editingGrade.id}`, updatedGrade);
      toast.success("Grade updated successfully!");
      setShowGradeDialog(false);
      fetchData();
    } catch (error) {
      console.error("Error updating grade:", error);
      toast.error("Failed to update grade");
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

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="spinner"></div>
      </div>
    );
  }

  const mySchedules = schedules.filter(s => s.teacher_id === user.id);
  const mySubjects = [...new Set(mySchedules.map(s => s.subject_code))];
  const myGrades = grades.filter(g => mySubjects.includes(g.subject_code));

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-blue-50">
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
              <p className="text-sm text-gray-500">Teacher ID: {user.id}</p>
            </div>
          </div>
          <Button data-testid="logout-btn" variant="ghost" size="sm" onClick={onLogout}>
            <LogOut className="w-4 h-4 mr-2" />
            Logout
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Dashboard Summary */}
        <div className="mb-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card data-testid="summary-card-classes" className="card-hover">
            <CardHeader className="pb-3">
              <CardDescription>Total Classes</CardDescription>
              <CardTitle className="text-3xl">{mySchedules.length}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">{mySubjects.length} subjects</p>
            </CardContent>
          </Card>

          <Card data-testid="summary-card-students" className="card-hover">
            <CardHeader className="pb-3">
              <CardDescription>Students Graded</CardDescription>
              <CardTitle className="text-3xl">{myGrades.length}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">Grade records</p>
            </CardContent>
          </Card>

          <Card data-testid="summary-card-complaints" className="card-hover">
            <CardHeader className="pb-3">
              <CardDescription>Pending Complaints</CardDescription>
              <CardTitle className="text-3xl">{complaints.length}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">Need attention</p>
            </CardContent>
          </Card>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="grades" className="space-y-6">
          <TabsList data-testid="dashboard-tabs" className="grid grid-cols-3 w-full max-w-2xl">
            <TabsTrigger value="grades" data-testid="tab-grades">
              <ClipboardList className="w-4 h-4 mr-2" />
              Manage Grades
            </TabsTrigger>
            <TabsTrigger value="schedule" data-testid="tab-schedule">
              <Calendar className="w-4 h-4 mr-2" />
              My Schedule
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
                <CardTitle>Student Grades Management</CardTitle>
                <CardDescription>Anna University Exam Pattern (Part A: 5×2=10, Part B: 5×8=40)</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {myGrades.map((grade) => (
                    <div key={grade.id} data-testid={`grade-${grade.id}`} className="p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <div>
                          <h4 className="font-semibold">{grade.student_name}</h4>
                          <p className="text-sm text-gray-500">{grade.subject} ({grade.subject_code})</p>
                        </div>
                        <div className="flex items-center gap-2">
                          <Badge className="text-lg px-4 py-1">{grade.grade}</Badge>
                          <Button data-testid={`edit-grade-${grade.id}`} size="sm" variant="outline" onClick={() => handleEditGrade(grade)}>
                            <Edit className="w-4 h-4" />
                          </Button>
                        </div>
                      </div>
                      <Separator className="my-2" />
                      <div className="grid grid-cols-3 gap-4 text-sm">
                        <div>
                          <p className="text-gray-500">Part A (10)</p>
                          <p className="font-semibold">{grade.part_a_marks}</p>
                        </div>
                        <div>
                          <p className="text-gray-500">Part B (40)</p>
                          <p className="font-semibold">{grade.part_b_marks}</p>
                        </div>
                        <div>
                          <p className="text-gray-500">Total (50)</p>
                          <p className="font-semibold text-lg">{grade.total_marks}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Schedule Tab */}
          <TabsContent value="schedule" data-testid="schedule-content">
            <Card>
              <CardHeader>
                <CardTitle>Class Schedule</CardTitle>
                <CardDescription>Your weekly timetable</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"].map((day) => {
                    const daySchedules = mySchedules.filter(s => s.day === day);
                    return (
                      <div key={day} data-testid={`schedule-${day}`}>
                        <h4 className="font-semibold mb-2">{day}</h4>
                        {daySchedules.length > 0 ? (
                          <div className="space-y-2">
                            {daySchedules.map((schedule) => (
                              <div key={schedule.id} className="p-3 bg-gray-50 rounded flex items-center justify-between">
                                <div>
                                  <p className="font-medium">{schedule.subject}</p>
                                  <p className="text-sm text-gray-500">{schedule.subject_code}</p>
                                </div>
                                <div className="text-right">
                                  <p className="text-sm font-medium">{schedule.time_slot}</p>
                                  <p className="text-sm text-gray-500">{schedule.room}</p>
                                </div>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <p className="text-sm text-gray-500 italic">No classes scheduled</p>
                        )}
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Complaints Tab */}
          <TabsContent value="complaints" data-testid="complaints-content">
            <Card>
              <CardHeader>
                <CardTitle>Student Complaints</CardTitle>
                <CardDescription>Review and respond to student issues</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {complaints.length === 0 ? (
                    <p className="text-center text-gray-500 py-8">No pending complaints</p>
                  ) : (
                    complaints.map((complaint) => (
                      <div key={complaint.id} data-testid={`complaint-${complaint.id}`} className="p-4 bg-gray-50 rounded-lg">
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <h4 className="font-semibold">{complaint.title}</h4>
                              <Badge variant="secondary">{complaint.complaint_type}</Badge>
                            </div>
                            <p className="text-sm text-gray-600 mb-2">{complaint.description}</p>
                            <p className="text-xs text-gray-400">
                              Submitted by {complaint.submitted_by_name} on {complaint.submitted_date}
                            </p>
                            {complaint.complaint_type === "public" && (
                              <p className="text-xs text-gray-500 mt-1">{complaint.votes} votes</p>
                            )}
                          </div>
                        </div>
                        <div className="mt-3">
                          <Button data-testid={`resolve-complaint-${complaint.id}`} size="sm" onClick={() => handleResolveComplaint(complaint.id)}>
                            Resolve Complaint
                          </Button>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>

      {/* Edit Grade Dialog */}
      <Dialog open={showGradeDialog} onOpenChange={setShowGradeDialog}>
        <DialogContent data-testid="grade-dialog">
          <DialogHeader>
            <DialogTitle>Edit Grade</DialogTitle>
            <DialogDescription>
              Update marks for {editingGrade?.student_name} - {editingGrade?.subject}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <Label htmlFor="part-a">Part A Marks (out of 10)</Label>
              <Input
                data-testid="part-a-input"
                id="part-a"
                type="number"
                min="0"
                max="10"
                value={gradeForm.part_a_marks}
                onChange={(e) => setGradeForm({ ...gradeForm, part_a_marks: e.target.value })}
              />
            </div>
            <div>
              <Label htmlFor="part-b">Part B Marks (out of 40)</Label>
              <Input
                data-testid="part-b-input"
                id="part-b"
                type="number"
                min="0"
                max="40"
                value={gradeForm.part_b_marks}
                onChange={(e) => setGradeForm({ ...gradeForm, part_b_marks: e.target.value })}
              />
            </div>
            <div className="p-3 bg-gray-50 rounded">
              <p className="text-sm text-gray-600">Total Marks: {parseInt(gradeForm.part_a_marks || 0) + parseInt(gradeForm.part_b_marks || 0)} / 50</p>
              <p className="text-sm text-gray-600">Grade: {calculateGrade(parseInt(gradeForm.part_a_marks || 0) + parseInt(gradeForm.part_b_marks || 0))}</p>
            </div>
            <Button data-testid="update-grade-btn" onClick={handleUpdateGrade} className="w-full">
              Update Grade
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default TeacherDashboard;