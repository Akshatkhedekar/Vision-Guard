from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from pathlib import Path

ROOT=Path(__file__).parent
OUT=ROOT/'reports'/'VisionGuard_Project_Report.pdf'
AS=ROOT/'data'/'sample'

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='CoverTitle', parent=styles['Title'], fontSize=25, leading=30, alignment=TA_CENTER, spaceAfter=18))
styles.add(ParagraphStyle(name='CoverSub', parent=styles['Normal'], fontSize=13, leading=18, alignment=TA_CENTER, spaceAfter=10))
styles.add(ParagraphStyle(name='H1x', parent=styles['Heading1'], fontSize=17, leading=21, spaceBefore=6, spaceAfter=10))
styles.add(ParagraphStyle(name='H2x', parent=styles['Heading2'], fontSize=12.5, leading=16, spaceBefore=7, spaceAfter=6))
styles.add(ParagraphStyle(name='Bodyx', parent=styles['BodyText'], fontSize=9.6, leading=14, spaceAfter=7))
styles.add(ParagraphStyle(name='Small', parent=styles['BodyText'], fontSize=8, leading=11))


def footer(canv, doc):
    canv.saveState(); canv.setFont('Helvetica',8); canv.drawString(2*cm,1.1*cm,'VisionGuard — Computer Vision Project'); canv.drawRightString(19*cm,1.1*cm,f'Page {doc.page}'); canv.restoreState()

def box_flow(labels):
    from reportlab.graphics.shapes import Drawing, Rect, String, Line
    d=Drawing(500,130)
    x=10
    for i,label in enumerate(labels):
        d.add(Rect(x,50,95,45,strokeColor=colors.black,fillColor=colors.whitesmoke,rx=5,ry=5))
        d.add(String(x+47.5,73,label[:18],fontSize=8,textAnchor='middle'))
        if i < len(labels)-1: d.add(Line(x+95,72,x+115,72,strokeWidth=1.2)); d.add(String(x+105,77,'>',fontSize=10,textAnchor='middle'))
        x += 120
    return d

story=[]
story += [Spacer(1,3.2*cm), Paragraph('VisionGuard', styles['CoverTitle']), Paragraph('Road Defect Detection & Severity Analysis', styles['CoverSub']), Spacer(1,1*cm), Paragraph('Computer Vision — VITyarthi Build Your Own Project', styles['CoverSub']), Spacer(1,2.2*cm), Paragraph('<b>Student:</b> Akshat Khedekar', styles['CoverSub']), Paragraph('<b>Reg. No.:</b> 24BAI10798', styles['CoverSub']), Paragraph('<b>Date:</b> 15 September 2026', styles['CoverSub']), Spacer(1,3*cm), Paragraph('Academic project report', styles['CoverSub']), PageBreak()]

story += [Paragraph('1. Introduction', styles['H1x']), Paragraph('Road infrastructure inspection often requires reviewing a large number of images. A computer-vision system can reduce repetitive manual screening by highlighting image regions that differ from their local road texture and by producing structured measurements. VisionGuard is an academic prototype built around this idea.', styles['Bodyx']), Paragraph('The system demonstrates a complete computer-vision workflow: image acquisition, preprocessing, local-contrast analysis, adaptive thresholding, morphological filtering, contour extraction, feature measurement, severity estimation, batch analytics, and report generation.', styles['Bodyx']), Paragraph('The project deliberately uses an interpretable classical OpenCV pipeline rather than requiring a large deep-learning model. This makes the system lightweight and allows the evaluator to observe how fundamental image-processing concepts contribute to the final result.', styles['Bodyx'])]

story += [Paragraph('2. Problem Statement', styles['H1x']), Paragraph('Manual road-image inspection is repetitive and may become difficult to scale when many images must be screened. The problem addressed by VisionGuard is to create a lightweight computer-vision prototype that accepts road images, detects candidate surface-defect regions, estimates their severity from image-derived features, and summarizes the results for review.', styles['Bodyx']), Paragraph('<b>Important scope boundary:</b> the output represents candidate regions rather than certified pothole labels. Environmental factors such as illumination, camera angle, road texture and image quality can affect the detection result.', styles['Bodyx'])]

story += [Paragraph('3. Objectives', styles['H1x'])]
for x in ['Apply fundamental computer-vision preprocessing techniques to real-world road imagery.', 'Detect candidate surface-defect regions using interpretable image-processing operations.', 'Extract geometric features from detected contours and convert them into a simple severity estimate.', 'Provide a usable interface for single-image and batch analysis.', 'Generate a concise PDF result report and maintain a modular, testable codebase.']:
    story.append(Paragraph('• '+x, styles['Bodyx']))

story += [Paragraph('4. Functional Requirements', styles['H1x'])]
fr=[['ID','Requirement','Input','Output'],['FR1','Image upload and validation','JPG/PNG road image','Validated image'],['FR2','Preprocessing','Image','Denoised/normalized image'],['FR3','Candidate defect detection','Processed image','Bounding regions'],['FR4','Feature extraction','Contours','Area, circularity, fill ratio'],['FR5','Severity analysis','Features','Low/Medium/High'],['FR6','Batch analytics','Multiple results','Aggregate statistics'],['FR7','Report generation','Summary','PDF report']]
t=Table(fr,colWidths=[1.2*cm,6.1*cm,4.0*cm,5.1*cm]); t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.4,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8),('VALIGN',(0,0),(-1,-1),'TOP')]))
story += [t, PageBreak()]

story += [Paragraph('5. Non-Functional Requirements', styles['H1x'])]
nfr=[['Requirement','Design response'],['Usability','Browser-based Streamlit dashboard with direct upload and visible results.'],['Performance','Image resizing bounds computation and classical CPU-based processing avoids mandatory GPU inference.'],['Reliability','Input validation, deterministic processing steps, and automated unit tests.'],['Maintainability','Preprocessing, detection, analytics and reporting are separated into modules.'],['Resource efficiency','No persistent database or mandatory deep-learning model is required.'],['Error handling','Empty/invalid image arrays raise explicit validation errors.']]
t=Table(nfr,colWidths=[4.2*cm,13.0*cm]); t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.4,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8.5),('VALIGN',(0,0),(-1,-1),'TOP')]))
story += [t, Spacer(1,15), Paragraph('6. System Architecture', styles['H1x']), box_flow(['Image Upload','Preprocess','Detect','Features','Severity','Analytics / PDF']), Spacer(1,12), Paragraph('The Streamlit user interface orchestrates four core source modules. The preprocessing module standardizes images. The detection module generates candidate regions and geometric measurements. The analytics module aggregates image-level results. The reporting module turns a summary into a PDF document.', styles['Bodyx'])]

story += [Paragraph('7. Process Workflow', styles['H1x']), Paragraph('1. The user uploads one or more road images. 2. Each image is resized if necessary and denoised. 3. The image is converted to grayscale and histogram equalization is applied. 4. Local contrast is computed by comparing blurred local intensity with the original blurred signal. 5. Adaptive thresholding creates a binary candidate mask. 6. Morphological opening/closing removes small noise and closes gaps. 7. External contours are extracted. 8. Contours outside the area limits are rejected. 9. Area, bounding-box geometry, circularity and fill ratio are measured. 10. A normalized score is mapped to Low, Medium or High severity. 11. Results are displayed and can be aggregated or exported.', styles['Bodyx']), PageBreak()]

story += [Paragraph('8. UML / Design Diagrams', styles['H1x']), Paragraph('Use Case Diagram — the primary actor is the User, who can upload images, view detections, inspect measurements, view batch analytics, and generate a PDF report.', styles['Bodyx']), Paragraph('Class/Component Diagram', styles['H2x']), box_flow(['Preprocessing','Detection','Analytics','Reporting']), Spacer(1,12), Paragraph('Sequence: User → Streamlit UI → Preprocessing → Detection → Analytics → Reporting. The reporting step is invoked only when the user requests a PDF.', styles['Bodyx']), Paragraph('Storage Design', styles['H2x']), Paragraph('No persistent database is required. Uploaded images are processed in memory. This design reduces unnecessary retention and keeps the academic prototype simple. Structured results are held as Python dictionaries and Pandas DataFrames during a session.', styles['Bodyx'])]

story += [Paragraph('9. Design Decisions & Rationale', styles['H1x']), Paragraph('<b>OpenCV:</b> selected because the project is intended to demonstrate fundamental image-processing operations such as filtering, thresholding, morphology and contours.', styles['Bodyx']), Paragraph('<b>Classical baseline:</b> selected for interpretability and low resource requirements. Each stage can be inspected and explained during a viva.', styles['Bodyx']), Paragraph('<b>Streamlit:</b> selected to expose the algorithm through a simple browser interface without requiring a separate frontend/backend deployment.', styles['Bodyx']), Paragraph('<b>Modular architecture:</b> separates concerns and supports unit testing and future replacement of the detection module with a trained detector.', styles['Bodyx'])]

story += [Paragraph('10. Implementation Details', styles['H1x']), Paragraph('<b>Preprocessing:</b> the input is resized to a bounded width, Gaussian-blurred to suppress high-frequency noise, converted to grayscale, and histogram-equalized.', styles['Bodyx']), Paragraph('<b>Candidate detection:</b> local contrast is estimated from blurred intensity differences. Adaptive thresholding produces a candidate mask, followed by elliptical morphological opening and closing.', styles['Bodyx']), Paragraph('<b>Feature extraction:</b> contours are filtered by area. For each accepted contour the system calculates area, bounding box, circularity, fill ratio and relative image area.', styles['Bodyx']), Paragraph('<b>Severity:</b> a transparent heuristic score combines normalized relative area and contour fill ratio. Thresholds map the score to Low, Medium or High. This is an academic heuristic rather than a medically/safety-certified or production inspection standard.', styles['Bodyx'])]

story += [Paragraph('11. Screenshots / Results', styles['H1x']), Paragraph('A synthetic sample road image was included in the repository so the evaluator can immediately demonstrate the pipeline without needing to find a dataset first. The sample contains three visually distinct dark surface regions.', styles['Bodyx'])]
img1=str(AS/'sample_road.jpg'); img2=str(AS/'sample_road_annotated.jpg')
story += [Image(img1,width=15.5*cm,height=10.3*cm), Spacer(1,5), Paragraph('Figure 1. Sample road image used for local demonstration.', styles['Small']), PageBreak(), Image(img2,width=15.5*cm,height=10.3*cm), Spacer(1,5), Paragraph('Figure 2. Annotated output produced by the OpenCV detector. The demonstration identified three candidate regions, each classified as Medium by the current heuristic.', styles['Small']), PageBreak()]

story += [Paragraph('12. Testing Approach', styles['H1x']), Paragraph('Automated tests are provided in tests/test_detection.py. They cover preprocessing shape preservation, detection output types, and severity-summary counting. The UI should additionally be checked manually by uploading JPG and PNG images and generating a PDF report.', styles['Bodyx'])]
tests=[['Test case','Expected outcome','Status'],['Preprocess valid image','Correct image and grayscale dimensions','PASS'],['Detect valid image','Annotated image + list returned','PASS'],['Summarize severity list','Correct totals and severity counts','PASS'],['Upload JPG/PNG through UI','Images displayed and analysed','Manual verification'],['Generate PDF','PDF is created and downloadable','Manual verification']]
t=Table(tests,colWidths=[6*cm,7.2*cm,3.8*cm]); t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.4,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8.2)])); story.append(t)

story += [Paragraph('13. Challenges Faced', styles['H1x']), Paragraph('The main design challenge is that road defects do not have a single visual appearance. Shadows, stains, lane markings and texture changes can resemble damaged areas. Instead of hiding this limitation, the project makes the detection pipeline interpretable and explicitly labels its outputs as candidate regions. This creates a clear basis for evaluating the baseline and replacing it with a learned detector later.', styles['Bodyx']), Paragraph('Another challenge is maintaining a useful demonstration without requiring a large model download. The chosen OpenCV pipeline keeps installation and execution lightweight while still showing multiple computer-vision concepts.', styles['Bodyx'])]

story += [Paragraph('14. Learnings & Key Takeaways', styles['H1x'])]
for x in ['Image preprocessing can substantially influence downstream segmentation.', 'Adaptive thresholding can handle local illumination differences better than a single global threshold in some scenes.', 'Morphological operations are useful for removing isolated noise and joining fragmented regions.', 'Contours provide an interpretable bridge between pixel-level masks and geometric measurements.', 'A complete CV system needs more than detection: validation, UI, analytics, testing and reporting make the prototype demonstrable.', 'Classical CV baselines are useful as interpretable reference systems even when a future version may use deep learning.']:
    story.append(Paragraph('• '+x, styles['Bodyx']))

story += [Paragraph('15. Future Enhancements', styles['H1x'])]
for x in ['Collect or use a labelled road-defect dataset and measure precision, recall, F1-score and IoU.', 'Train and compare a supervised object detector or segmentation model against the classical baseline.', 'Add video/frame-by-frame analysis for dashcam footage.', 'Add geotagging and map-based inspection history where appropriate and privacy-compliant.', 'Calibrate severity using labelled expert assessments rather than heuristic thresholds.', 'Add model monitoring, confidence thresholds and human review for ambiguous detections.']:
    story.append(Paragraph('• '+x, styles['Bodyx']))

story += [Paragraph('16. References', styles['H1x']), Paragraph('1. OpenCV documentation and Python OpenCV APIs used for image processing, filtering, thresholding and contours.', styles['Bodyx']), Paragraph('2. Streamlit documentation for the interactive Python application interface.', styles['Bodyx']), Paragraph('3. NumPy and Pandas documentation for numerical processing and tabular analysis.', styles['Bodyx']), Paragraph('4. VITyarthi Build Your Own Project instructions supplied for this submission.', styles['Bodyx']), PageBreak()]

story += [Paragraph('17. Repository & Submission Checklist', styles['H1x'])]
check=[['Item','Included'],['README.md','Yes'],['statement.md','Yes'],['Source code','Yes'],['5–10 meaningful modules/files','Yes'],['Requirements/configuration','Yes'],['Tests','Yes'],['Architecture/workflow/UML documentation','Yes'],['Sample data','Yes'],['Project report PDF','Yes'],['Git repository metadata','Yes']]
t=Table(check,colWidths=[11*cm,5.5*cm]); t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.4,colors.grey),('BACKGROUND',(0,0),(-1,0),colors.lightgrey),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('ALIGN',(1,1),(-1,-1),'CENTER'),('FONTSIZE',(0,0),(-1,-1),8.5)])); story.append(t)
story += [Spacer(1,12), Paragraph('The repository is designed to be pushed directly to GitHub. Before final submission, replace the clone URL placeholder in README.md with the actual repository URL and add any course-specific cover-page or faculty requirements if your instructor has additional instructions.', styles['Bodyx'])]

doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=1.8*cm,leftMargin=1.8*cm,topMargin=1.6*cm,bottomMargin=1.8*cm)
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
