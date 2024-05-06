using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR;
using UnityEngine.XR.Hands;
using System;

public class HandDataLogger : MonoBehaviour
{
    // Start is called before the first frame update
    public XRHand rHand;
    XRHandSubsystem m_HandSubsystem;
    public TextMesh xPos;
    public TextMesh yPos;
    public TextMesh zPos;
    Vector3 pos;
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
        if (updateType == XRHandSubsystem.UpdateType.Dynamic)
        {
            // var indexTip = 11;
            // IT IS THIS LINE RIGHT HERE OFFICER THIS ONE
            // IS THE ONE THAT IS CAUSING THE CRASH ON STARTUP
            // for (var i = XRHandJointID.BeginMarker.ToIndex();
            //          i < XRHandJointID.EndMarker.ToIndex();
            //          i++)
            // {

            //     // activityText.text = XRHandJointID.IndexTip.ToIndex().ToString();

            // }
            var trackingData = rHand.GetJoint(XRHandJointID.IndexTip);
            xPos.text = rHand.ToString();
            if (trackingData.TryGetPose(out Pose pose))
            {
                xPos.text = "x" + pose.position.x.ToString();
                yPos.text = "y" + pose.position.y.ToString();
                zPos.text = "z" + pose.position.z.ToString();
            }

        }
    }

    void Update()
    {
        // activityText.text = "Updating correctly";

    }
}
