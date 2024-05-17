using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR;
using UnityEngine.XR.Hands;
using System.IO;
using System;

public class HandDataLogger : MonoBehaviour
{
    // Start is called before the first frame update
    public XRHand rHand;
    XRHandSubsystem m_HandSubsystem;
    public TextMesh xPos;
    public TextMesh yPos;
    public TextMesh zPos;
    public TextMesh trackingStatus;
    Vector3 pos;
    public bool isTracking = false;
    public int curTrial;
    private StreamWriter logWriter;
    private DateTime logStartTime;
    public bool frombelow = true;
    public float yThresh;
    public GameObject cube;
    public string[] attributes = {"x_pos", "y_pos", "z_pos"};

    void Start()
    {
        // activityText.text = "Hello World";
        // activityText = GetComponent<TextMesh>();
        xPos.text = "Oh my god please work";
        pos = new Vector3(0, 0, 0);

        // Set up the hand subsystem
        var handSubsystems = new List<XRHandSubsystem>();
        // rHand = GetComponent<XRHand>();
        SubsystemManager.GetSubsystems(handSubsystems);

        for (var i = 0; i < handSubsystems.Count; ++i)
        {
            xPos.text = "This is a test";
            var handSubsystem = handSubsystems[i];
            if (handSubsystem.running)
            {
                xPos.text = "Subsystem is running";
                m_HandSubsystem = handSubsystem;
                xPos.text = "m_subsystem != null => " + (m_HandSubsystem != null).ToString();
                // Why is this break here ?
                break;
            }

            xPos.text = "Made it ouside of break condition";

            // if the handsubsystem is running, it breaks and this is never reached?
        }
        if (m_HandSubsystem != null)
        {
            m_HandSubsystem.updatedHands += OnUpdatedHands;
            rHand = m_HandSubsystem.rightHand;
            xPos.text = "OnUpdatedHands was added";
        }
        else
        {
            xPos.text = "Hand subsystem was null";
        }

        // activityText.text = handSubsystems.Count.ToString();

    }

    // Update is called once per frame


    void OnUpdatedHands(XRHandSubsystem subsystem,
        XRHandSubsystem.UpdateSuccessFlags updateSuccessFlags,
        XRHandSubsystem.UpdateType updateType)
    {
        // if (updateType == XRHandSubsystem.UpdateType.Dynamic)
        // {
            // This gets the joint of the right hand
        var trackingData = rHand.GetJoint(XRHandJointID.IndexTip);
        xPos.text = rHand.ToString();
        if (trackingData.TryGetPose(out Pose pose))
        {
            xPos.text = "x: " + pose.position.x.ToString();
            yPos.text = "y: " + pose.position.y.ToString();
            zPos.text = "z: " + pose.position.z.ToString();

            if (pose.position.z > 0.6 && !isTracking && frombelow)
            {
                frombelow = false;
                yThresh = pose.position.y;
                cube.transform.position = new Vector3(0.002350986f, yThresh - 0.5f, 0.25f);
                isTracking = !isTracking;
                StartLogging();
                StartCoroutine(pause());
            }
            else if (pose.position.z > 0.6 && isTracking && frombelow)
            {
                isTracking = !isTracking;
                frombelow = false;
                StopLogging();
            }

            if (pose.position.z < 0.6)
            {
                frombelow = true;
            }

            if (isTracking && frombelow)
            {
                LogAttributes(pose.position);
            }


        }
        // }
    }

    IEnumerator pause()
    {
        yield return new WaitForSeconds(0.5f);
    }

    void StartLogging()
    {
        curTrial += 1;

        string filename = $"handTrail_{curTrial:D2}.csv";
        string path = Path.Combine(Application.persistentDataPath, filename);

        logWriter = new StreamWriter(path);
        logWriter.WriteLine(GetLogHeader());

        logStartTime = DateTime.UtcNow;
        trackingStatus.text = "TRACKING";

    }

    string GetLogHeader()
    {
        string logHeader = "time,";

        logHeader += String.Join(",", attributes);
        
        return logHeader;
    }

    void StopLogging()
    {
        logWriter.Close();
        trackingStatus.text = "NOT TRACKING";
    }


    void LogAttributes(Vector3 posVector)
    {

        if (posVector.y > yThresh + 0.05f)
        {
            return;
        }
        TimeSpan timeDifference = DateTime.UtcNow - logStartTime;

        string logValue = $"{timeDifference.TotalMilliseconds},";

        logValue += $"{posVector.x},{posVector.y},{posVector.z}";

        logWriter.WriteLine(logValue);

    }

    void Update()
    {
        // activityText.text = "Updating correctly";

    }
}
